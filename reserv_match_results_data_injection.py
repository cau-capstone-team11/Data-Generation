import pymysql
import csv
import random
import string
import numpy as np
DB_Host = "3.16.229.70"

SCHEDULE_ID = 0
RESERV_TEAM_ID = 1
OPPONENT_TEAM_ID = 2
FAC_ID = 3
GYM_ID = 4
SUBJ_ID = 5
MIN_PARTICIPANT = 6
MAX_PARTICIPANT = 7
IS_SOLO = 8


# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111', db='lifesports', charset='utf8')
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

print("DB connection successfully constructed.")

sql_reservMatches = "SELECT S.schedule_ID, R.reserv_team_ID, R.opponent_team_ID, S.fac_ID, S.gym_ID, S.subj_ID,S.min_participant, S.max_participant, R.is_solo \
FROM lifesports.fac_schedule AS S JOIN lifesports.reserv_matches AS R ON S.schedule_ID = R.reserv_ID \
WHERE S.subj_ID = '1' and S.schedule_type = '1';"

sql_teamMembers = "SELECT * FROM lifesports.team_user_list"

curs.execute(sql_reservMatches)
list_reservMatches = curs.fetchall()

curs.execute(sql_teamMembers)
list_allTeamMembers = curs.fetchall()

file_result = open('match_result.sql','w')
file_members = open('match_participant.sql', 'w')

insert_matchResult = "INSERT INTO lifesports.match_result VALUES "
insert_matchParticipant= "INSERT INTO lifesports.match_participant VALUES "

print(len(list_allTeamMembers))

for match in list_reservMatches :
    
    s1 = random.randrange(5)
    s2 = random.randrange(5)
    matchID = match[SCHEDULE_ID]
    gymID = match[GYM_ID]
    facID = match[FAC_ID]
    subjID = match[SUBJ_ID]
    score = str(max(s1,s2)) +':' + str(min(s1,s2))
    memCountPerTeam = int(random.randrange(match[MIN_PARTICIPANT], match[MAX_PARTICIPANT] + 1) / 2)

    if match[IS_SOLO] == 1 : # 내전        
        print("[ 내전 ]")

#        print("gymID = ", gymID, "facID = ", facID, "subjID = ", subjID, "score = ", score)
        winTeamID = max(match[RESERV_TEAM_ID], match[OPPONENT_TEAM_ID])
        loseTeamID = min(match[RESERV_TEAM_ID], match[OPPONENT_TEAM_ID])
        list_teamMembers = []

        for i in range(len(list_allTeamMembers)) :
            if list_allTeamMembers[i][0] == winTeamID :
                list_teamMembers.append(list_allTeamMembers[i])

        print("winTeamID = ", winTeamID, "loseTeamID = ", loseTeamID)
        print("team명단 = ", list_teamMembers)

        mvpUDID = list_teamMembers[random.randrange(len(list_teamMembers))][1]

        temp = '(' + str(matchID) + ','
        temp += str(winTeamID) + ',' + str(loseTeamID) + ','
        temp += str(gymID) + ',' + str(facID) + ',' + str(subjID) + ','
        temp += '\'' + score + '\',' + str(mvpUDID) + ');\n'
        
        sql = insert_matchResult + temp
        file_result.write(sql)
#        print(sql)

        for line in list_teamMembers :
            temp = '(' + str(matchID) + ','
            temp += str(line[1]) + ',0);\n'
            sql = insert_matchParticipant + temp
#            print(sql)
            file_members.write(sql)
    else : # team vs team
        print("[ team vs team ]")
        list_winParticipants = []
        list_loseParticipants = []
        winTeamIdx = random.randrange(1,3)
        loseTeamIdx = 3 - winTeamIdx
        winTeamID = match[winTeamIdx]
        loseTeamID = match[loseTeamIdx]
        print("Win team ID : ", winTeamID, ", Lose team ID : ", loseTeamID)

        list_winTeamMembers = []
        list_loseTeamMembers = []
        for i in range(len(list_allTeamMembers)) :
            if list_allTeamMembers[i][0] == winTeamID :
                list_winTeamMembers.append(list_allTeamMembers[i])
            if list_allTeamMembers[i][0] == loseTeamID :
                list_loseTeamMembers.append(list_allTeamMembers[i])

        memCountPerTeam = min(len(list_winTeamMembers), len(list_loseTeamMembers), memCountPerTeam)

#        print("Win team members : ", list_winTeamMembers)
 #       print("Lose team members : ", list_loseTeamMembers)

        for i in range(memCountPerTeam) :
            idx = random.randrange(len(list_winTeamMembers))
            list_winParticipants.append(list_winTeamMembers[idx])
            del list_winTeamMembers[idx]

            idx = random.randrange(len(list_loseTeamMembers))
            list_loseParticipants.append(list_loseTeamMembers[idx])
            del list_loseTeamMembers[idx]

#        print("Win participant : ", list_winParticipants)
#        print("Lose participant : ", list_loseParticipants)

        mvpUDID = list_winParticipants[random.randrange(len(list_winParticipants))][1]

        temp = '(' + str(matchID) + ','
        temp += str(winTeamID) + ',' + str(loseTeamID) + ','
        temp += str(gymID) + ',' + str(facID) + ',' + str(subjID) + ','
        temp += '\'' + score + '\',' + str(mvpUDID) + ');\n'
            
        sql = insert_matchResult + temp
        file_result.write(sql)
#        print(sql)
        for line in list_winParticipants :
            temp = '(' + str(matchID) + ','
            temp += str(line[1]) + ',1);\n'
            sql = insert_matchParticipant + temp
#            print(sql)
            file_members.write(sql)

        for line in list_loseParticipants :
            temp = '(' + str(matchID) + ','
            temp += str(line[1]) + ',0);\n'
            sql = insert_matchParticipant + temp
#            print(sql)
            file_members.write(sql)

file_result.close()
file_members.close()

conn.commit()
# Connection 닫기
conn.close()

