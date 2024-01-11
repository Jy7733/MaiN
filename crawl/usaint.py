import requests
from bs4 import BeautifulSoup

login_url = "https://smartid.ssu.ac.kr/Symtra_sso/smln_pcs.asp"
crawl_url = "https://saint.ssu.ac.kr/irj/portal"

session = requests.session()

params = dict()
params['in_tp_bit'] = '0'
params['rast_cause_cd'] = '03'
params['userid'] = '20213080'
params['pwd'] = 'amy16041604!!'

res = session.post(login_url, data=params)
# print(session.cookies.get_dict())

res = session.get(crawl_url)
soup = BeautifulSoup(res.content,'html.parser')
# data = soup.select('body > div > div.main_wrap > div.main_left > div.main_box09 > div.main_box09_con_w > ul > li:nth-child(1) > dl > dd > a > strong')
data = soup.select('body > div > div.main_wrap > div.main_left > div.main_box09 > div.box_top > p.access_text')

for item in data :
    print(item.get_text())