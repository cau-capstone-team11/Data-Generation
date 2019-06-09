import pymysql
import csv
import random
import string
import numpy as np
DB_Host = "3.16.229.70"

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111', db='lifesports', charset='utf8')
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

print("DB connection successfully constructed.")

sql_select = 'SELECT * FROM team'
curs.execute(sql_select)
list_team = curs.fetchall()

teamCount = len(list_team)
mmr = []
winning_rate = []

for i in range(teamCount) :
    mmr.append(int(random.gauss(2000,400)))

for i in range(teamCount) :
    winning_rate.append(round(((mmr[i] - min(mmr))/(max(mmr) - min(mmr)) * 0.2 + random.randrange(38,45) * 0.01) * 100, 2))

sql_update = 'UPDATE lifesports.team SET team_MMR = %s, winning_rate = %s where team_ID = %s'
for i in range(teamCount) :
    insertTuple = (str(mmr[i]),str(winning_rate[i]),str(i+1))
    curs.execute(sql_update,insertTuple)
    print(insertTuple)

conn.commit()
# Connection 닫기
conn.close()
