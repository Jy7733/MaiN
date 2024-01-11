#AI융합학부 공지사항
import requests
from bs4 import BeautifulSoup
import mysql.connector      
from datetime import datetime

#url
url = 'http://aix.ssu.ac.kr/notice.html?searchKey=ai&page=' #ai융합학부 공지 페이지

#beautifulsoup 객체 생성
response = requests.get(url + "1")
soup = BeautifulSoup(response.text, 'html.parser')

#데이터베이스 연결
conn = mysql.connector.connect(
    host = 'main-db.cb6mac662yc2.us-east-1.rds.amazonaws.com',
    user = 'admin',
    password = 'wodudtnalsduswo1228',
    database = 'main_schema'
)

curs = conn.cursor()

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

            #이미 존재하는 공지인지 확인
            curs.execute("SELECT COUNT(*) FROM ai_noti WHERE title = %s", (title,))
            if curs.fetchone()[0] > 0:
                continue  # 이미 존재하면 다음 아이템으로 넘어감

            sql = "INSERT INTO ai_noti(title,link,date) VALUES (%s, %s, %s)" #ai_noti 테이블에 삽입
            val = (title,link,date)
            curs.execute(sql,val)
            conn.commit()
    
    curs.execute("SELECT COUNT(*) FROM ai_noti")  # 크롤링 후 데이터의 개수를 확인
    count_after = curs.fetchone()[0]  # fetchone()은 결과를 튜플로 반환하므로 [0]을 사용해 개수를 가져옴

    # print(count_before,",", count_after)
    if count_before == count_after:  # 크롤링 전 후의 데이터 개수가 같다면 while문을 멈춤
        break
    page+=1

conn.close()
