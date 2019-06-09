import pymysql
import csv
import random
import string
import numpy as np

# n개의 알파벳으로 구성된 random 문자열 생성
def randUpWord(n):
    word = ''
    for i in range(0,n):
        word = word + random.choice(string.ascii_letters)
    return word

# n개의 random 알파벳 문자열 뒤에 m개의 random 숫자 추가 (datatype : string)
def randUpWordNum(n,m):
    word = randUpWord(n)
    for i in range(0,m):
        word = word + str(random.randrange(0,10))
    return word


DB_Host = "3.16.229.70"

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111', db='lifesports', charset='utf8')
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

print("DB connection successfully constructed.")

sql_selectUserTable = "SELECT UDID FROM user"
curs.execute(sql_selectUserTable)
list_userID = curs.fetchall()

conn.commit()
# Connection 닫기
conn.close()

print("User data completely imported")

max_memCount = 50
min_memCount = 22
max_teamCount = int(len(list_userID) / min_memCount)
teamMemCount = 0

list_teamMemCount = []

notOrgdUserCnt = len(list_userID)

for i in range(max_teamCount) :

    if notOrgdUserCnt < max_memCount :
        break
    teamMemCount = random.randrange(min_memCount,max_memCount + 1)
    notOrgdUserCnt -= teamMemCount
    list_teamMemCount.append(teamMemCount)

npTeamMemCnt = np.asarray(list_teamMemCount, dtype = int)   

TEAM_ID = 0
UDID = 1

orgdUserCnt = npTeamMemCnt.sum()
teamMemInfo = np.zeros((orgdUserCnt,2), dtype = int)
teamLeaderInfo = np.zeros((len(list_teamMemCount),2), dtype = int)
isLeader = 0

i = 0 # (i = 0 ~ (ordUserCnt - 1))
while i < orgdUserCnt :
    teamIdx = random.randrange(0,len(list_teamMemCount))

    if npTeamMemCnt[teamIdx] > 0 :
        npTeamMemCnt[teamIdx] -= 1
        teamMemInfo[i][TEAM_ID] = (teamIdx + 1)
        teamMemInfo[i][UDID] = i + 1
        if teamLeaderInfo[teamIdx][UDID] == 0 and random.randrange(0,100) < 30 :
            teamLeaderInfo[teamIdx][TEAM_ID] = teamIdx + 1
            teamLeaderInfo[teamIdx][UDID] = i + 1
        i += 1
    else :
        continue

print("Team info generation completed.")

file = open("team_data_injection.sql","w")

sql_Insert = 'INSERT INTO lifesports.team (team_ID,team_name,team_leader_UDID,team_MMR,team_main_subj,winning_rate) VALUES \n'

mmr = []


for i in range(len(list_teamMemCount)) :
    line = '(' + str(teamLeaderInfo[i][TEAM_ID]) + ',\''
    line += randUpWordNum(random.randrange(4,7),random.randrange(2,5)) + '\',' 
    line += str(teamLeaderInfo[i][UDID]) + ','
    line += str('%.0f' % random.gauss(2000,400)) + ',\'1\','
    line += str('%.1f' % random.gauss(50,5)) + ')'

    sql_Insert += line

    if i < (len(list_teamMemCount) - 1) :
        sql_Insert += ',\n'
    
file.write(sql_Insert)
file.close()

file = open('team_user_list_data_injection.sql', 'w')

sql_Insert = 'INSERT INTO lifesports.team_user_list (team_ID,UDID) VALUES \n'

for i in range(orgdUserCnt) :
    line = '(' + str(teamMemInfo[i][TEAM_ID]) + ',' + str(teamMemInfo[i][UDID]) + ')'
    sql_Insert += line

    if i < (orgdUserCnt - 1) :
        sql_Insert += ',\n'

file.write(sql_Insert)
file.close()