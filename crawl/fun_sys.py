#펀시스템 공지사항
import requests
from bs4 import BeautifulSoup
import mysql.connector      
from datetime import datetime

#url
url = 'https://fun.ssu.ac.kr/ko/program/all/list/all/' #펀시스템 공지 페이지

#beautifulsoup 객체 생성
response = requests.get(url + "1")
soup = BeautifulSoup(response.text, 'html.parser')

#데이터베이스 연결
conn = mysql.connector.connect(
    # host = 'main-db.cb6mac662yc2.us-east-1.rds.amazonaws.com',
    # user = 'admin',
    # password = 'wodudtnalsduswo1228',
    # database = 'main_schema'
    host = 'localhost',
    user = 'root',
    password = '0000',
    database = 'new_schema'
)

curs = conn.cursor()

page = 1
while True :
    response = requests.get(url + str(page))
    soup = BeautifulSoup(response.text,'html.parser')
    data = soup.find_all('li')

    curs.execute("SELECT COUNT(*) FROM funsys_noti")
    count_before = curs.fetchone()[0]

    for item in data :
        title_link = item.find('a')
        if title_link :
            title_tag = title_link.find('b', class_='title')

            if title_tag is not None : 
                title = title_link.find('b', class_='title').get_text() #공지 제목
                link = "https://fun.ssu.ac.kr/"+title_link['href'] #공지 링크 

                times = item.find_all('time') 
                if times :
                    start_date = times[0]['datetime'].split('T')[0] #신청 시작 날짜
                    end_date = times[1]['datetime'].split('T')[0] #신청 마감 날짜 

                    #이미 존재하는 공지인지 확인
                    # curs.execute("SELECT COUNT(*) FROM funsys_noti WHERE title = %s", (title,))
                    curs.execute("SELECT COUNT(*) FROM funsys_noti WHERE title = %s AND start_date = %s", (title, start_date))

                    if curs.fetchone()[0] > 0:
                        continue  # 이미 존재하면 다음 아이템으로 넘어감

                    sql = "INSERT INTO funsys_noti(title,link,start_date,end_date) VALUES (%s, %s, %s, %s)" #funsys_noti 테이블에 삽입
                    val = (title,link,start_date,end_date)
                    curs.execute(sql,val)
                    conn.commit()
        
    curs.execute("SELECT COUNT(*) FROM funsys_noti")  # 크롤링 후 데이터의 개수를 확인
    count_after = curs.fetchone()[0]  # fetchone()은 결과를 튜플로 반환하므로 [0]을 사용해 개수를 가져옴

    if count_before == count_after:  # 크롤링 전 후의 데이터 개수가 같다면 while문을 멈춤
        break
    page+=1

conn.close()
