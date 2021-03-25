from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
import starter as st
import time
# 秀泰

def get_event(url='https://www.showtimes.com.tw/events?corpId=4'):
    driver = st.start_drive()
    driver.get(url)
    time.sleep(5)  # 確定js跑完結果才傳回html
    page_html = driver.page_source
    # print(page_html)
    soup = BeautifulSoup(page_html, 'html.parser')
    driver.close()
    return soup


def get_movie_name(soup):
    # 找出所有的電影名稱

    mn = soup.find_all("p", {"class": "font-bold font-purple nobottommargin", "style": "font-size: 1.2em;"})
    dic = {}
    movie_name_list = []
    for y in mn:
        name = y.text
        movie_name_list.append(name)

    return movie_name_list


def get_date(soup):
    # 先將可以提供的日期先抓下來
    t = soup.find("select", attrs={"class": "pull-right form-control",
                                   "style": "margin-right: 10px; margin-bottom: 10px; width: 130px;"})
    t = t.find_all("option")
    date_list_for_url = []
    date_list_for_db = []
    for x in t:
        date_list_for_db.append(x.text)
        date_list_for_url.append("&date=" + x.text.replace("-", "/"))

    return date_list_for_url, date_list_for_db

    # 找出一天的每部電影的時刻


def get_today_time(soup):
    movie_time = soup.find_all("table", {"class": "visible-xs", "style": "width: 100%; margin-top: 10px;"})
    time_list = []

    for z in movie_time:  # 每部電影
        each_movie = z.find_all("div")
        tmp = []
        for k in each_movie:  # 每個時刻
            tmp.append(k.text[:5])
        time_list.append(tmp)

    return time_list


def excute_webcrawler4():
    soup = get_event()
    date_list_for_url, date_list_for_db = get_date(soup)
    result = []
    for everyday_url_index in range(len(date_list_for_url)):
        print(date_list_for_url[everyday_url_index])
        everyday_soup = get_event(
            url="https://www.showtimes.com.tw/events?corpId=4" + date_list_for_url[everyday_url_index])
        movie_name_for_one_day = get_movie_name(everyday_soup)
        time_list = get_today_time(everyday_soup)
        transfer_time_list = []
        for trans in time_list:
            trans_list2 = []
            for trans_in_list in trans:
                final_time = date_list_for_db[everyday_url_index][5:].replace("-", "/") + " " + trans_in_list
                print(final_time)
                trans_list2.append(final_time)

            transfer_time_list.append(trans_list2)

        print(transfer_time_list)

        # 打包成Json
        dic_1 = {}
        for link_index in range(len(movie_name_for_one_day)):
            dic_1['Name'] = movie_name_for_one_day[link_index]
            for every_movie_time in transfer_time_list[link_index]:
                dic_1['Time'] = every_movie_time
                dic_1['theater'] = "秀泰影城"
                result.append(dic_1.copy())

    print(result)
    return result
