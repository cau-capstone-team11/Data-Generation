import pymysql
import csv


DB_Host = "3.16.229.70"
inputFileName = "Seoul_public_PE_Facilities.csv"

inpuFile = open(inputFileName, 'r', encoding = 'utf-8')
csv_reader = csv.reader(inpuFile)
gym_data = []
subjects = []
gym_info = []
#    0  /   1    /        2        /  3  /   4  /  5  /    6    /        7       /   8      /  9      /    10
# 자치구 /  분류  /      시설명     / 주소 / 위도 /경도 / 전화번호 /      종목       / 홈페이지 / 강습여부 / 실내`실외
# 종로구 / 체육관 / 종로문화체육센터 /  -   /  -  /  -  /   -     / 수영 헬스 에어 ~ /     -   /   유,무  / 실내,실외

# gym_ID / gym_name / gym_fig / gym_location / gym_lat / gym_longi / avail_starttime / avail_endtime / gym_info / admin_ID

# MySQL Connection 연결
conn = pymysql.connect(host=DB_Host, user='root', password='1111',
                       db='lifesports', charset='utf8')
 
# Connection 으로부터 Cursor 생성
curs = conn.cursor()

for line in csv_reader :
    subjects = line[7].split(' ')
    if '축구' in subjects or '야구' in subjects or '농구' in subjects or '배드민턴' in subjects :
        gym_data.append(line)

for line in gym_data :
    gym_name = line[2]
    gym_location = line[3]
    gym_latitude = line[4]
    gym_longitude = line[5]
    gym_info = "체육관 내 이용 가능 종목 : " + line[7]
    if line[6] != '-' :
        gym_info += "\n\n체육관 전화번호 : " + line[6]
    if line[8] != '-' :
        gym_info += "\n\n체육관 홈페이지 : " + line[8]
    gym_info += "\n\n강습 여부 : " + line[9]
    gym_info += "\n\n실내 / 실외 : " + line[10]

    sqlInsert = "INSERT INTO gym(gym_name,gym_location,gym_latitude,gym_longitude,gym_info) VALUES (%s,%s,%s,%s,%s)"
    insertVarTuple = (gym_name, gym_location, gym_latitude, gym_longitude, gym_info)
    curs.execute(sqlInsert, insertVarTuple)


curs.execute("select count(*) from gym")
rows = curs.fetchall()
     
print(rows)     # 전체 rows
conn.commit()
# Connection 닫기
conn.close()