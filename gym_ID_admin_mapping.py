import pymysql
import csv


DB_Host = "3.16.229.70"

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111',
                       db='lifesports', charset='utf8')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

sqlSelect = "select UDID, gym_ID from gym_admin"
curs.execute(sqlSelect)
sqlUpdate = "update gym set gym_admin_ID = %s where gym_ID = %s"
results = curs.fetchall()
print(results)

for line in results :
    updateTuple = (line[0], line[1])
    curs.execute(sqlUpdate, updateTuple)

conn.commit()
# Connection 닫기
conn.close()