import pymysql
import random
import time
import math
import string
import numpy as np
#gym_admin table

# ID / PWD / name / gender / birth / email / phone / gym_ID
# insert into gym_admin(ID, PWD, name, gender, birth, email, phone, gym_ID) values('star7357', HEX(AES_ENCRYPT('dlehdgus13', 'lifesports')),'Lee,Donghyun', 'male', '1995-07-18', 'star7357@naver.com', '010-8948-8330', 3);

DB_Host = "3.16.229.70"

xtime = 3600                                    
yn = ['Y','N']                                  
sex = ['M','F']
emailAddr = ['@gmail.com', '@naver.com', '@daum.net', "@hanmail.net", "@gmail.com", "@gmail.com", "@gmail.com", "naver.com"]
lastName = ['김', '김','김', '김', '김', '김', '김', '김', '김', '김', '이', '이', '이', '이', '이', '이', '이', '이', '이',
            '박', '박','박', '박', '박', '박', '박', '송', '정', '조', '방', '최', '최', '최', '최', '소', '공', '금', '강'] 
firstName = ['동현','강현','찬형','형석','현석','하연','다혜','다현','원재','주현','상현','도훈','현진','성현','석현','다인',
             '예지','예형','주현','주영','주혁','류경','민준','민주','수혁','시현','동혁','주연','진모','예슬','찬기','혁재',
             '연빈','명엽','현주','지영','나연','민수','병윤','성현','태홍','건희','여진','광진','재균','재욱','혁준','승은',
             '효주','주용','동민','준환','태웅','건우','경현','기현','기환','미송','상욱','상혁','성재','영현','정현','정연',
             '동주','석규','준영','혜수','혜준','희준','현우','재훈','준성','진호','용호','승재','승국','재민','희진','준혁']

# 'yyyymmdd'형식으로 xtime이후의 시간 random 생성
def randtimestamp(startDate,rand):  #startDate : 시작 날짜, rand : 시작날짜 ~ 시작날짜 + rand 사이에서 random date 생성 
    randtime = time.strftime("%Y-%m-%d", time.gmtime(xtime+(random.randrange(0,rand)*86400)))
    return randtime

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

random.seed(time.time())

flags = np.zeros(208, dtype = int)
temp = 0
count = 0

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111',
                       db='lifesports', charset='utf8')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

#실질적으로 Schema 구성이 들어가는 부분
for j in range (0,220):

    # ID / PWD / name / gender / birth / email / phone / gym_ID

    ID = randUpWordNum(random.randrange(4,6),random.randrange(2,4))

    PWD = '1111'
    name = lastName[random.randrange(0,len(lastName))] + firstName[random.randrange(0,len(lastName))]
    gender = sex[random.randrange(0,len(sex))]
    birth = randtimestamp(xtime, 7300)
    email = ID + emailAddr[random.randrange(0, len(emailAddr))]
    phone = '010-' + randUpWordNum(0,4) + '-' + randUpWordNum(0,4)
        
    while(1) :
        temp = random.randrange(5,208)
        if flags[temp] == 0 :
            gym_ID = temp
            flags[temp] = 1
            count += 1
            break
        if count >= 203 : 
            gym_ID = None
            break
    sqlInsert = "insert into gym_admin(ID, PWD, name, gender, birth, email, phone, gym_ID) values(%s, HEX(AES_ENCRYPT(%s,'lifesports')),%s, %s, %s, %s,%s,%s);"
    insertTuple = (ID, PWD, name, gender, birth, email,phone,gym_ID)
    curs.execute(sqlInsert, insertTuple)
#    print(insertTuple)

curs.execute("select count(*) from gym_admin")
rows = curs.fetchall()

print(rows)
conn.commit()
conn.close()