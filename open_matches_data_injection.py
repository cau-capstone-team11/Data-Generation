import pymysql
import random
import time
import math
import string
import numpy as np

DB_Host = "3.16.229.70"

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111',
                       db='lifesports', charset='utf8')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

sql_getAvailOpenMatches = "SELECT schedule_ID,min_participant,max_participant FROM fac_schedule WHERE schedule_type = 2 "
curs.execute(sql_getAvailOpenMatches)
list_availOpenMatchSchedule = curs.fetchall()

sql_getUserCount = "SELECT count(*) FROM user"
curs.execute(sql_getUserCount)
userCount = curs.fetchone()[0]

#sql_insert = "INSERT INTO open_matches (reserv_ID, subj_ID, UDID) VALUES (%s,%s,%s)"
reservRate = 95

teamList = []
print(len(list_availOpenMatchSchedule))

file = open('open_matches_data_injection.sql', 'w')

sql_Insert = 'INSERT INTO lifesports.open_matches (reserv_ID, subj_ID, UDID) VALUES'

for line in list_availOpenMatchSchedule :

    if random.randrange(100) > reservRate : 
        continue
    reserv_ID = line[0]
    min_participant = line[1]
    max_participant = line[2]
    participantSet = set()
    if min_participant == max_participant :
        participantCount = min_participant
    else :
        participantCount = random.randrange(min_participant, max_participant)

    while len(participantSet) < participantCount :
        participantSet.add(random.randrange(userCount))

    list_participants = list(participantSet)


    for userID in list_participants :
        insertTuple = (reserv_ID, '1', userID)
#        print(insertTuple)
        temp = sql_Insert + '(' + str(reserv_ID) + ',1,' + str(userID) + ');\n'
        file.write(temp)
#        curs.execute(sql_insert,insertTuple)

#(reserv_ID, 1, UDID)
curs.fetchall()
conn.commit()
conn.close()

file.close()