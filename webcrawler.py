from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
import os
import starter as st
import time

# Lux cinema

def prepare():
    response = requests.get("https://www.luxcinema.com.tw/web/2020.php?type=ShowTimes#type_anchor")
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all("div", {"class": "col-md-9"})
    return soup, result


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


# 拿名字
def get_name(result):
    name = []
    for i in result:
        n = i.find("h1").text
        n = n[:-4]
        name.append(n)
    # print(len(name))

    return name


# 拿URL 還要處理
def get_href(soup):
    film_url = []
    f = soup.find("div", {"class": "movie_all_list"})

    for i in f.find_all('a'):
        film_url.append("https://www.luxcinema.com.tw/web/" + i.get('href'))

    # print(film_url)

    return film_url


# 拿到月、日、場次時間
def get_time(url="https://www.luxcinema.com.tw/web/2020-movie_item.php?film_id=1879"):
    day = []
    date_and_time = []
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    month = s.find("span", {"class": "month"}).text
    daylist = s.find_all("span", {"class": "day"})
    for zz in daylist:
        day.append(month + "/" + zz.text)

    # 找出所有場次的時間和日期
    time_list = s.find_all("div", {"class": "time_list"})
    for i in range(len(time_list)):
        time_for_link = []
        for j in time_list[i].find_all("b"):
            time_for_link.append(j.text[:5])

        for k in time_for_link:  # 將日期和時間傳出成為一個list
            date_and_time.append(day[i] + " " + k)

    # Link for get_seat_count
    link = s.find_all("div", {"class": "time_list"})
    urlforseat = []
    for j in link:
        z = j.find_all("a")
        for k in z:
            urlforseat.append("https://www.luxcinema.com.tw/web/" + k.get('href'))

    return date_and_time, urlforseat


def get_link(url="https://www.luxcinema.com.tw/web/2020-movie_item.php?film_id=1850"):
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    # print(s)


def get_seat_count(url='https://www.luxcinema.com.tw/web/2020_sel_ticket.php?serial_number=dfe884434a156c03f92d887873b6b370&film_id=1879&showdate=0&showtime=2021-03-24&sel_ticket_id=129586&seat_type=SEAT'):
    driver = st.start_drive()
    driver.get(url)
    driver.execute_script("ticket_Plus(324,2)")
    driver.execute_script("ticket_Plus(41,2)")
    driver.execute_script("ticket_function()")
    b = driver.page_source
    s = BeautifulSoup(b, "html.parser")
    resu = s.find_all("img", {"src": "images/lux_btn/lux_seat_01.png"})
    # print(len(resu))
    driver.close()

    return len(resu)

# get_name > get_href >
# get_time()
def excute_webcrawler():
    soup, result = prepare()
    name = get_name(result)
    url = get_href(soup)
    webresult = []
    try:
        for i in range(len(name)):
            dic_1 = {'Name': name[i]}
            time, seat_url = get_time(url[i])
            # print(dic_1)
            # print(time)
            for index in range(len(time)):
                dic_1['Time'] = time[index]
                seat = get_seat_count(seat_url[index])
                print(seat)
                dic_1['seat'] = seat
                dic_1['theater'] = "樂聲影城"
                print(dic_1)
                webresult.append(dic_1.copy())
                # print(webresult)
    except:
        pass

    
    return webresult
