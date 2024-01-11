#SSU Catch공지사항
import requests
from bs4 import BeautifulSoup
import mysql.connector      
from datetime import datetime   


url = 'https://scatch.ssu.ac.kr/%EA%B3%B5%EC%A7%80%EC%82%AC%ED%95%AD/page/' #ssu:catch 공지 페이지

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
while True:
    response = requests.get(url + str(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all('div', class_='row no-gutters align-items-center')

    curs.execute("SELECT COUNT(*) FROM ssucatch_noti")
    count_before = curs.fetchone()[0]

    for item in data:
        title_link = item.find('a')
        if title_link:
            date_str =item.select_one('div[class^="h2 text-info font-weight-bold"]').get_text() #게시 날짜 
            date = datetime.strptime(date_str, '%Y.%m.%d').date()

            link = title_link['href'] #공지 링크 

            title = title_link.find('span', class_='d-inline-blcok m-pt-5').get_text().strip() #공지 제목

            category = item.find('span', class_='label d-inline-blcok border pl-3 pr-3 mr-2').get_text().strip() #카테고리 (학사/ 장학 등..)

            progress = item.find('div',class_='notice_col2').get_text()  #진행/완료 
            if not progress.strip(): #진행/완료 가 없으면 None할당
                progress = None
                               
            #제목이 같은 공지가 있는지 확인
            curs.execute("SELECT COUNT(*) FROM ssucatch_noti WHERE title = %s", (title,))
            if curs.fetchone()[0] > 0: #제목이 일치하는 데이터가 있다면 
                # title이 일치하는 row의 progress 값을 update
                sql = "UPDATE ssucatch_noti SET progress = %s WHERE title = %s"
                curs.execute(sql, (progress, title))
                continue
            else: #제목이 일치하는 데이터가 없다면 
                # 새로운 공지사항을 insert
                sql = "INSERT INTO ssucatch_noti(title,link,date,category,progress) VALUES (%s, %s, %s, %s, %s)"
                val = (title, link, date, category, progress)
                curs.execute(sql, val)    
                conn.commit()

    curs.execute("SELECT COUNT(*) FROM ssucatch_noti")
    count_after = curs.fetchone()[0]

    # 페이지에 새로운 데이터가 없다면, 크롤링 종료
    if count_before == count_after:
        break

    # 다음 페이지로 이동
    page += 1

conn.close()
