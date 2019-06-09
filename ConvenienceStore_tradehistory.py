import pymysql
import time
import random
import datetime

DB_Host = "3.16.229.70"

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111', db='convenience_store', charset='utf8')

 # Connection 으로부터 Cursor 생성
curs = conn.cursor()

sql_select = "SELECT * from tradehistory"
curs.execute(sql_select)

list_tradehistory = curs.fetchall()
for line in list_tradehistory :
    print(line)

conn.commit()
# Connection 닫기
conn.close()