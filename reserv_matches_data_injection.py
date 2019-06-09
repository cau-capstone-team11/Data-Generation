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

sql_getFacSchedule = "SELECT schedule_ID,gym_ID FROM fac_schedule WHERE schedule_type = 1"
sql_getTeamID = "SELECT team_ID from team"
sql_gymID = "SELECT gym_ID FROM gym WHERE subj_info like '%축구%'"
sql_insertRMs = "INSERT INTO lifesports.reserv_matches (reserv_ID, subj_ID, reserv_team_ID,opponent_team_ID,is_solo) VALUES "

curs.execute(sql_gymID)
total_gymID = curs.fetchall()

list_gymID = []
for line in total_gymID :
    list_gymID.append(line[0])

soccerFieldCount = len(list_gymID)

curs.execute(sql_getFacSchedule)
list_facSchedule = curs.fetchall()

curs.execute(sql_getTeamID)
list_teamID = curs.fetchall()

MAX_HOME_TEAM = 3
list_homeStadium = np.zeros((soccerFieldCount,MAX_HOME_TEAM), dtype = int)
list_homeTeamCount = np.zeros(soccerFieldCount, dtype = int)

temp = 0
teamIdx = 1
while teamIdx <= len(list_teamID) :
    temp = random.randrange(soccerFieldCount)
    if list_homeTeamCount[temp] < MAX_HOME_TEAM :
        list_homeStadium[temp][list_homeTeamCount[temp]] = teamIdx
        list_homeTeamCount[temp] += 1
        teamIdx += 1
    else :
        continue      

reservRate = 95 

# resev_ID / subj_ID / reserv_team_ID / opponent_team_ID / is_solo
#                         0     ,    1  
#list_schedule[k] = (schedule_ID, gym_ID)

file = open('reserv_matches_data_injection.sql', 'w')

print(len(list_facSchedule))
for line in list_facSchedule :
    gym_Idx = list_gymID.index(line[1])

    if random.randrange(0,100) > reservRate or list_homeTeamCount[gym_Idx] == 0 :
        continue

    reserv_ID = line[0]
    subj_ID = 1
    reserv_team_ID = list_homeStadium[gym_Idx][random.randrange(list_homeTeamCount[gym_Idx])]
    if random.randrange(100) < 90 : # team vs team
        is_solo = 0
        while True :
            opponent_team_ID = random.randrange(len(total_gymID)) + 1
            if opponent_team_ID != reserv_team_ID and opponent_team_ID != 0 :
                break

    else :
        is_solo = 1
        opponent_team_ID = -1
    
    
# resev_ID / subj_ID / reserv_team_ID / opponent_team_ID / is_solo

    sql = "(" + str(reserv_ID) + ','
    sql += str(subj_ID) + ','
    sql += str(reserv_team_ID) + ','
    sql += str(opponent_team_ID) + ','
    sql += str(is_solo) + ');\n'

    temp = sql_insertRMs + sql

    file.write(temp)

file.close()


curs.fetchall()
conn.commit()
conn.close()