import pymysql
import random
import time
import math
import string
import numpy as np

DB_Host = "3.16.229.70"

#   0  /      1    /        2      /        3         /    4   /   5 /     6
# UDID / main_foot / main_position / subjective_skill / career / MMR / mvp_point

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111',
                       db='lifesports', charset='utf8')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

list_mainFoot = ['L','R']
list_mainPosition = ['GK','DF','MF','FW']
list_subjectiveSkill = ['상','중','하']

sql_select = "SELECT UDID from user"
curs.execute(sql_select)
list_userID = curs.fetchall()

for i in range(len(list_userID)) :

    UDID = list_userID[i][0]
    main_foot = list_mainFoot[random.randrange(len(list_mainFoot))]
    main_position = list_mainPosition[random.randrange(len(list_mainFoot))]
    subjective_skill = list_subjectiveSkill[random.randrange(len(list_subjectiveSkill))]
    career = random.randrange(2,37) # 3년차 정도 된 서비스라 가정

    sql_Insert = "INSERT INTO soccer_record (UDID,main_foot,main_position,subjective_skill,career) VALUES (%s,%s,%s,%s,%s)"
    insertTuple = (UDID, main_foot, main_position, subjective_skill, career)

    curs.execute(sql_Insert, insertTuple)
    print(insertTuple)

curs.execute("select count(*) from user")
rows = curs.fetchall()

print(rows)
conn.commit()
conn.close()