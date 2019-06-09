import pymysql
import time
import random

DB_Host = "3.16.229.70"

def randAvailTime() :
    avail_starttime = time.strftime("%H:%M:%S", time.gmtime(random.randrange(9,18)*1800))
    avail_endtime = time.strftime("%H:%M:%S", time.gmtime(random.randrange(33,44)*1800))
    return avail_starttime, avail_endtime

# gym_ID / avail_starttime / avail_endtime / avail_participant / fac_name / subj_ID
sqlInsert = "insert into fac_info(gym_ID,avail_starttime,avail_endtime,avail_participant,fac_name,subj_ID) values (%s,%s,%s,%s,%s,%s)"
#insertTuple = (gym_ID, avail_starttime, avail_endtime, avail_participant, fac_name, subj_ID)

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111',
                       db='lifesports', charset='utf8')
 # Connection 으로부터 Cursor 생성
curs = conn.cursor()

sqlSelect = "select gym_ID, avail_starttime, avail_endtime, subj_info from gym"
curs.execute(sqlSelect)
subjPerGym = curs.fetchall()

for gym in subjPerGym :
    print(gym)
    gym_ID = gym[0]
    avail_starttime = gym[1]
    avail_endtime = gym[2]
    try : 
        avail_subj = gym[3].split(' ')
    except :
        avail_sub = ''

    if '축구' in avail_subj :
        subj_ID = 1
        subjCount = random.randrange(1, 3)
        for i in range(subjCount) :
            fac_name = "축구장" + str(i + 1)
            insertTuple = (gym_ID, avail_starttime, avail_endtime, str(26), fac_name, subj_ID)
            curs.execute(sqlInsert, insertTuple)

    if '야구' in avail_subj :
        subj_ID = 2
        subjCount = 1
        fac_name = "야구장" + str(i + 1)
        insertTuple = (gym_ID, avail_starttime, avail_endtime, str(20), fac_name, subj_ID)
        curs.execute(sqlInsert, insertTuple)
    
    if '농구' in avail_subj :
        subj_ID = 3
        subjCount = random.randrange(1, 3)
        for i in range(subjCount) :
            fac_name = "농구장" + str(i + 1)
            insertTuple = (gym_ID, avail_starttime, avail_endtime, str(14), fac_name, subj_ID)
            curs.execute(sqlInsert, insertTuple)

    if '배드민턴' in avail_subj :
        subj_ID = 4
        subjCount = random.randrange(2, 9)
        for i in range(subjCount) :
            fac_name = "배드민턴장" + str(i + 1)
            insertTuple = (gym_ID, avail_starttime, avail_endtime, str(4), fac_name, subj_ID)
            curs.execute(sqlInsert, insertTuple)

curs.execute("select count(*) from fac_info")
rows = curs.fetchall()

print(rows)

conn.commit()
# Connection 닫기
conn.close()