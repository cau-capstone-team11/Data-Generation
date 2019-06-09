import pymysql
import time
import random
import datetime

CUSTOMER_CNT = 1000
STORE_CNT = 100

now = datetime.datetime.now()

def purchase() :
    memberID = random.randrange(CUSTOMER_CNT)
    storeID = random.randrange(STORE_CNT)
    isDiscount = random.randrange(2)
    isMembership = random.randrange(2)
    purchaseTime = now.strftime('%Y-%m-%d %H:%M:%S')
    cardNum = random.randrange(10000000, 99999999)

    return memberID, storeID, isDiscount, isMembership, purchaseTime, cardNum

DB_Host = "3.16.229.70"

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111', db='convenience_store', charset='utf8')

 # Connection 으로부터 Cursor 생성
curs = conn.cursor()

sql_insert = "INSERT INTO tradehistory (memberID, storeID, isDiscount, isPoint, tradeDate, cardNumber) VALUES (%s,%s,%s,%s,%s,%s)"
tuple_insert = purchase()

curs.execute(sql_insert, tuple_insert)
print(tuple_insert)

conn.commit()
# Connection 닫기
conn.close()