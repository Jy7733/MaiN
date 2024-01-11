from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

# 로그인 페이지로 이동
driver.get('https://smartid.ssu.ac.kr/Symtra_sso/smln.asp?apiReturnUrl=https%3A%2F%2Fsaint.ssu.ac.kr%2FwebSSO%2Fsso.jsp')

# 로그인 정보 입력
driver.find_element(By.NAME,'userid').send_keys('20213080')  
driver.find_element(By.NAME,'pwd').send_keys('amy16041604!!')

# 로그인 버튼 클릭
driver.find_element(By.CSS_SELECTOR,'#sLogin > div > div.area_login > form > div > div:nth-child(2) > a').click() 

cookies = driver.get_cookies()
# print(cookies)

s = requests.Session()

for cookie in cookies :
    s.cookies.set(cookie['name'],cookie['value'])

response = s.get("https://saint.ssu.ac.kr/webSSUMain/main_student.jsp")
print(response.text)

# driver.get("https://saint.ssu.ac.kr/webSSUMain/main_student.jsp")

# for cookie in cookies :
#     driver.add_cookie(cookie)

# 로그인 후 페이지가 완전히 로딩될 때까지 기다림
# elem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div > div.main_wrap > div.main_left > div.main_box09 > div.main_box09_con_w > ul > li:nth-child(1) > dl > dd > a'))) 
# WebDriverWait(driver,60).until(EC.url_to_be("https://saint.ssu.ac.kr/webSSUMain/main_student.jsp"))
# print(elem.text)
# time.sleep(5)
# BeautifulSoup 객체 생성
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# print(driver.page_source)

# 페이지 정보 출력
# check_name = soup.find('p', class_='main_title')
# print(check_name)

# WebDriver 종료
driver.quit()
