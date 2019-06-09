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

sql_select = 'SELECT count(*) FROM soccer_record'
curs.execute(sql_select)
userCount = curs.fetchone()[0]

mmr = []
mvp_point = []

for i in range(userCount) :
    mmr.append(int(random.gauss(2000,400)))

for i in range(userCount) :
    mvp_point.append(int((mmr[i] - min(mmr))/(max(mmr) - min(mmr)) * 500 + random.randrange(0,50)))

sql_update = 'UPDATE lifesports.soccer_record SET MMR = %s, mvp_point = %s where UDID = %s'
for i in range(userCount) :
    insertTuple = (str(mmr[i]),str(mvp_point[i]),str(i+1))
    curs.execute(sql_update,insertTuple)

conn.commit()
# Connection 닫기
conn.close()
