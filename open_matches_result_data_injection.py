import pymysql
import random
import string
import numpy as np
DB_Host = "3.16.229.70"

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111', db='lifesports', charset='utf8')
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

print("DB connection successfully constructed.")

sql_scheduleInfo = "SELECT schedule_ID,gym_ID,fac_ID,subj_ID FROM fac_schedule WHERE schedule_type = 2"
sql_openMatches = "SELECT * FROM lifesports.open_matches"


curs.execute(sql_scheduleInfo)
list_scheduleInfo = curs.fetchall()

curs.execute(sql_openMatches)
list_openMatches = curs.fetchall()

conn.commit()
# Connection 닫기
conn.close()

SCHEDULE_ID = 0
GYM_ID = 1
FAC_ID = 2
SUBJ_ID = 3

file_results = open('openMatches_result.sql', 'w')
flie_participants = open('openMatches_participants.sql', 'w')

sql_results = 'INSERT INTO lifesports.match_result VALUES '
sql_participants = 'INSERT INTO lifesports.open_match_participant VALUES '

for schedule in list_scheduleInfo :

    s1 = random.randrange(5)
    s2 = random.randrange(5)
    score = str(max(s1,s2)) +':' + str(min(s1,s2))
    matchID = schedule[SCHEDULE_ID]
    gymID = schedule[GYM_ID]
    facID = schedule[FAC_ID]
    subjID = schedule[SUBJ_ID]
    list_participants = []
    list_teamA = []
    list_teamB = []
    list_teamID = [-100,-200]

    is_A_win = random.randrange(2) # is_A_win == 1 : A win!!

    for i in range(len(list_openMatches)) :
        if list_openMatches[i][SCHEDULE_ID] == schedule[SCHEDULE_ID] :
            list_participants.append(list_openMatches[i][2])

    if len(list_participants) == 0 :
        continue

    for i in range(len(list_participants)) :
        if i % 2 == 0 :
            list_teamA.append(list_participants[i])
        else :
            list_teamB.append(list_participants[i])

    if is_A_win == 1 :
        mvpUDID = list_teamA[random.randrange(len(list_teamA))]
        winTeamID = list_teamID[0]
        loseTeamID = list_teamID[1]
    else :
        mvpUDID = list_teamB[random.randrange(len(list_teamB))]
        winTeamID = list_teamID[1]
        loseTeamID = list_teamID[0]

    temp = '(' + str(matchID) + ','
    temp += str(winTeamID) + ',' + str(loseTeamID) + ','
    temp += str(gymID) + ',' + str(facID) + ',' + str(subjID) + ','
    temp += '\'' + score + '\',' + str(mvpUDID) + ');\n'

    sql = sql_results + temp
    file_results.write(sql)
#    print(sql)

    for i in range(len(list_teamA)) :
        temp = '(' + str(matchID) + ','
        temp += str(list_teamA[i]) + ',1);\n'
        sql = sql_participants + temp
#        print(sql)
        flie_participants.write(sql)
    
    for i in range(len(list_teamB)) :
        temp = '(' + str(matchID) + ','
        temp += str(list_teamB[i]) + ',0);\n'
        sql = sql_participants + temp
#        print(sql)
        flie_participants.write(sql)


file_results.close()
flie_participants.close()