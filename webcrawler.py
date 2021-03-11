from bs4 import BeautifulSoup
import requests
import re
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Lux cinema

response = requests.get("https://www.luxcinema.com.tw/web/2020.php?type=ShowTimes#type_anchor")
soup = BeautifulSoup(response.text, "html.parser")
result = soup.find_all("div", {"class": "col-md-9"})


def has_class_but_no_id(tag):
    return tag.has_attr('class') and not tag.has_attr('id')


# 拿名字
def get_name():
    name = []
    for i in result:
        n = i.find("h1").text
        n = n[:-4]
        name.append(n)
    print(len(name))

    return name


# 拿URL 還要處理
def get_href():
    film_url = []
    f = soup.find("div", {"class": "movie_all_list"})

    for i in f.find_all('a'):
        film_url.append("https://www.luxcinema.com.tw/web/" + i.get('href'))

    print(film_url)

    return film_url


# 拿到月、日、場次時間
def get_time(url="https://www.luxcinema.com.tw/web/2020-movie_item.php?film_id=1850"):
    day = []
    date_and_time = []
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    month = s.find("span", {"class": "month"}).text
    daylist = s.find_all("span", {"class": "day"})
    for zz in daylist:
        day.append(month + "/" + zz.text)

    time_list = s.find_all("div", {"class": "time_list"}, limit=2)
    time1 = []
    time2 = []
    for k in time_list:
        time1 = k.find_all("b")
        for x in time1:
            check = x.text
            check = check[:5]
            time2.append(check)
            print(time2)
        for y in time2:
            date_and_time.append(day[0] + " " + y)

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
    print(s)


def get_seat_count(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    driver.execute_script("ticket_Plus(326,2)")
    driver.execute_script("ticket_function()")
    b = driver.page_source
    s = BeautifulSoup(b, "html.parser")
    resu = s.find_all("img", {"src": "images/lux_btn/lux_seat_01.png"})
    print(len(resu))
    driver.close()

    return len(resu)


# get_name > get_href >
# get_time()

name = get_name()
url = get_href()
webresult = []
for i in range(len(name)):
    try:
        dic_1 = {'Name': name[i]}
        time, seat_url = get_time(url[i])
        for index in range(len(time)):
            dic_1['Time'] = time[index]
            seat = get_seat_count(seat_url[index])
            dic_1['seat'] = seat
            webresult.append(dic_1)
            print(webresult)
    except:
        pass
# print(webresult)

# print(day)
