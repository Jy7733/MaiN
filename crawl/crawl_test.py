#AI융합학부 공지사항
import requests
from bs4 import BeautifulSoup
import mysql.connector      
from datetime import datetime

#url 과 웹 드라이버 서비스 설정
url = 'http://aix.ssu.ac.kr/notice.html?searchKey=ai&page=' #ai융합학부 공지 페이지

#beautifulsoup 객체 생성
response = requests.get(url + "1")
soup = BeautifulSoup(response.text, 'html.parser')

#데이터베이스 연결
conn = mysql.connector.connect(
    host = 'database-1.cpiuim4gi0cd.ap-southeast-2.rds.amazonaws.com',
    user = 'admin',
    password = 'wotndudals1228',
    database = 'new_schema'
)

curs = conn.cursor()

curs.execute("SELECT MAX(date) FROM ai_noti") #가장 최근 업데이트 날짜 확인
latest_crawled_date = curs.fetchone()[0] 

page = 1
while True :
    response = requests.get(url + str(page))
    soup = BeautifulSoup(response.text,'html.parser')
    data = soup.find_all('tr')

    curs.execute("SELECT COUNT(*) FROM ai_noti")
    count_before = curs.fetchone()[0]

    for item in data :
        title_link = item.find('a')
        if title_link :
            title = title_link.get_text() #공지 제목
            link = "http://aix.ssu.ac.kr/"+title_link['href'] #공지 링크 
            date_str = item.find_all('td')[2].get_text() #게시 날짜

            date = datetime.strptime(date_str,'%Y.%m.%d').date()
            if latest_crawled_date is not None and date <= latest_crawled_date :
                break

            sql = "INSERT INTO ai_noti(title,link,date) VALUES (%s, %s, %s)" #ai_noti 테이블에 삽입
            val = (title,link,date)
            curs.execute(sql,val)
            conn.commit()
    
    curs.execute("SELECT COUNT(*) FROM ai_noti")  # 크롤링 후 데이터의 개수를 확인
    count_after = curs.fetchone()[0]  # fetchone()은 결과를 튜플로 반환하므로 [0]을 사용해 개수를 가져옴

    if count_before == count_after:  # 크롤링 전 후의 데이터 개수가 같다면 while문을 멈춤
        break
    page+=1

conn.close()
