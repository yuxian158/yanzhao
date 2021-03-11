import requests
import pymongo
from bs4 import BeautifulSoup
import time
first_url = "https://yz.chsi.com.cn/zsml/queryAction.do"
base_url = "https://yz.chsi.com.cn"

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.tanzhao
collection = db.school


def get_Examination_scope(url, school_name, city):
    html = requests.get(url).text
    html = BeautifulSoup(html, 'lxml')
    res1 = html.find(name='table', attrs={"class": "zsml-condition"}).find_all(name='tr')
    Department = res1[1].find(attrs={"class": "zsml-summary"}).get_text()  # 院系所
    major = res1[2].find(attrs={"class": "zsml-summary"}).get_text()  # 专业
    Research_direction = res1[3].find(attrs={"class": "zsml-summary"}).get_text()  # 研究方向
    Number = res1[4].find(attrs={"class": "zsml-summary"}).get_text()  # 研究方向
    res2 = html.find(name="tbody", attrs={"class": "zsml-res-items"}).tr.find_all(name="td")
    curriculum1 = res2[0].get_text()
    curriculum2 = res2[1].get_text()
    curriculum3 = res2[2].get_text()
    curriculum4 = res2[3].get_text()
    doc = {
                "school_name":school_name,"city":city,"Department":Department,"major":major,"Research_direction":Research_direction,
                "Number":Number,"curriculum1":curriculum1,"curriculum2":curriculum2,"curriculum3":curriculum3,"curriculum4":curriculum4
           }
    print(doc)
    time.sleep(0.2)
    collection.insert_one(doc)

def get_major_list(major_url, school_name, city):
    res = requests.get(major_url).text
    soup = BeautifulSoup(res, 'lxml')
    table_tab_lists = soup.find(name='table', attrs={"class": "ch-table more-content"}).tbody.find_all(name="tr")
    for table_tab in table_tab_lists:
        Examination_scope = (table_tab.find_all(name="td")[7].a['href'])
        get_Examination_scope(base_url+Examination_scope, school_name, city)


for i in range(1, 6):
    first_data = {
        "mldm": "zyxw",
        "yjxkdm": "0858",
        "zymc": "能源动力",
        "xxfs": 1,
        "pageno": i
    }
    page = requests.post(first_url, data=first_data).text
    html = BeautifulSoup(page, 'lxml')
    table_tab_lists = html.find(name='table', attrs={"class": "ch-table"}).tbody.find_all(name="tr")
    for table_tab in table_tab_lists:
        major_url = base_url + table_tab.find(name="a")['href']
        school_name = table_tab.find(name="a").get_text()
        city = table_tab.find_all(name="td")[1].get_text()
        get_major_list(major_url, school_name, city)
        time.sleep(1)
