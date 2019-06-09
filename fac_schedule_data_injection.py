#-*-coding:utf-8

import pymysql
import time
import random
import numpy as np

DB_Host = "3.16.229.70"

random.seed(time.time())

xtime = 1554076800            # 2019/4/1(UTC)
#xtime = 1556668800           # 2019/5/1


randDateInterval = 72      # 랜덤하게 스케줄을 생성할 날짜 간격 (일수)
# 'yyyymmdd'형식으로 xtime이후의 시간 random 생성
def randtimestamp(startDate,rand):  #startDate : 시작 날짜, rand : 시작날짜 ~ 시작날짜 + rand 사이에서 random date 생성 
    randtime = time.strftime("%Y-%m-%d", time.gmtime(xtime+(random.randrange(0,rand)*86400)))
    return randtime

def tickToRealTime(elapsedDate, tick) :
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(xtime + elapsedDate * 86400 + int(tick / 2) * 3600 + int(tick%2) * 1800 ))

def createReservSchedule(startTick, endTick) :
    list_scheduleTick = np.zeros(48, dtype = int)
    hourElapsed = startTick
    closedRate = random.randrange(0,100)
    # 95% 확률로 일정 생성
    if closedRate < 95 :
        while hourElapsed < (endTick - 4) and hourElapsed >= startTick :
            scheduleGenRate = random.randrange(0, 100)
            if scheduleGenRate < 60 : # 60% 확률로 예약 경기 생성
                interval = 3
                for i in range(hourElapsed, hourElapsed + interval) :
                    list_scheduleTick[i] = 1
                    hourElapsed += 1
            elif scheduleGenRate < 70 : # 10% 확률로 오픈 매칭 생성
                interval = 3
                for i in range(hourElapsed, hourElapsed + interval) :
                    list_scheduleTick[i] = 2
                    hourElapsed += 1
            elif scheduleGenRate < 95 : # 25% 확률로 아무런 일정 생성 x
                list_scheduleTick[hourElapsed] = 0
                hourElapsed +=1

            else : # 5% 확률로 토너먼트
                interval = 4 
                for i in range(hourElapsed, hourElapsed + interval) :
                    list_scheduleTick[i] = 4
                    hourElapsed += 1

    # 5% 확률로 휴관일 생성
    else :
        for i in range (startTick, endTick) :
            list_scheduleTick[i] = 3
    return list_scheduleTick


#list_gymInfo = []

# gym_ID / fac_ID / schedule_name / schedule_type / starttime / endtime

sqlSelect = "select gym_ID,fac_ID,avail_starttime,avail_endtime,subj_ID from fac_info"



# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111', db='lifesports', charset='utf8')
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

#list_gymInfo - [0] : gym_ID, [1] : fac_ID, [2] : avail_starttime, [3] : avail_endtime, [4] : subj_ID
curs.execute(sqlSelect)
list_gymInfo = curs.fetchall()


sqlInsert = "insert into lifesports.fac_schedule(gym_ID,fac_ID,subj_ID,schedule_name,schedule_type,starttime,endtime,min_participant,max_participant) values\n"

for line in list_gymInfo :

#    print(line[4])
    if line[4] != 1 :
        continue
    
    count = 0

#    print("fac_info : ",line)
    t = time.strptime(str(line[2]),"%H:%M:%S")
    startTick = int(t[3] * 2 + t[4] / 30)

    t = time.strptime(str(line[3]),"%H:%M:%S")
    endTick = int(t[3] * 2 + t[4] / 30)

#    print("startTick : ", startTick, ", endTick : ", endTick)
    list_schedule = []

    for elapsedDate in range(0, randDateInterval) :
        list_scheduleTick = np.zeros(48, dtype = int)
        scheduleGenRate = random.randrange(0, 10)
        if scheduleGenRate < 6 :    #60% 확률로 해당 날짜의 스케줄 생성
            list_scheduleTick = createReservSchedule(startTick,endTick)
        else : 
            continue
        
        i = startTick
        while i < (endTick - 4) :
            if list_scheduleTick[i] == 0 :
                i += 1
            elif list_scheduleTick[i] == 1 :
                list_schedule.append((1,tickToRealTime(elapsedDate, i), tickToRealTime(elapsedDate,i+3)))
                i += 3
            elif list_scheduleTick[i] == 2 :
                list_schedule.append((2,tickToRealTime(elapsedDate, i), tickToRealTime(elapsedDate,i+3)))
                i += 3
            elif list_scheduleTick[i] == 3 :
                list_schedule.append((3, tickToRealTime(elapsedDate,startTick), tickToRealTime(elapsedDate,endTick)))
                i += (endTick - startTick)
            else :
                list_schedule.append((4, tickToRealTime(elapsedDate,i),tickToRealTime(elapsedDate,i + 4)))
                i += 4
        
    #gym_ID, fac_ID, subj_ID, schedule_name, schedule_type, starttime, endtime, min_participant, max_participant

    #list_gymInfo - [0] : gym_ID, [1] : fac_ID, [2] : avail_starttime, [3] : avail_endtime, [4] : subj_ID

    reserv_count = 0
    open_count = 0
    holiday_count = 0
    tournament_count = 0

    print("list_schedule length : ",len(list_schedule))
    for j in range(count, len(list_schedule)) :
        
#        print(list_schedule[j])
        if list_schedule[j][0] == 1 :
            reserv_count += 1
            schedule_name = '예약 경기' + str(reserv_count)
        elif list_schedule[j][0] == 2 :
            open_count += 1
            schedule_name = '오픈 매칭' + str(open_count)
        elif list_schedule[j][0] == 3 :
            holiday_count += 1
            schedule_name = '휴관일' + str(holiday_count)
        elif list_schedule[j][0] == 4 :
            tournament_count += 1
            schedule_name = '토너먼트' + str(tournament_count)
        else : 
            schedule_name = "ERROR"

        # (gym_ID,fac_ID,subj_ID,schedule_name,schedule_type,starttime,endtime,min_participant,max_participant)
        sql = '(' + str(line[0]) + ','
        sql += str(line[1]) + ','
        sql += str(1) + ','
        sql += '\'' + schedule_name + '\','
        sql += str(list_schedule[j][0]) + ','
        sql += '\'' + str(list_schedule[j][1]) + '\','
        sql += '\'' + str(list_schedule[j][2]) + '\','
        sql += str(22) + ','
        sql += str(random.randrange(22, 27)) + '),\n'

        sqlInsert += sql
        count += 1

#        if j < (len(list_schedule) - 1) :
#            sqlInsert += ',\n'


file = open('fac_schedule_data_injection.sql', 'w')
file.write(sqlInsert)
file.close()


conn.commit()
# Connection 닫기
conn.close()