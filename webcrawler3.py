from bs4 import BeautifulSoup
import requests
import datetime


# 國賓
def url_trans():
    now_time = datetime.datetime.now()
    date_list = []
    day_list = []

    for i in range(5):
        p = str(now_time.date() + datetime.timedelta(days=i)).replace("-", "/")
        date_list.append(p)

    url = []
    for time_in_url in date_list:
        u = 'https://www.ambassador.com.tw/home/Showtime?ID=84b87b82-b936-4a39-b91f-e88328d33b4e&DT=' + time_in_url
        url.append(u)

    # print(url)

    return url

# url_trans()


def get_time(url='https://www.ambassador.com.tw/home/Showtime?ID=84b87b82-b936-4a39-b91f-e88328d33b4e&DT=2021/03/18'):
    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'html.parser')
    a = soup.find_all('div', {'class': 'showtime-item'})
    day = url[-5:]
    result = []
    for j in a:
        time = j.find_all('h6')
        movie_name = j.find_all('a', limit=3)[2].find(text=True)
        # print(movie_name)
        dic_1 = {'Name': movie_name}
        for x in time:
            dic_1['Time'] = day + " " + x.text.replace(' ', '')
            dic_1['theater'] = ['國賓大戲院']
            result.append(dic_1.copy())


    # print(result)

    return result
# print(result)
# get_time()


def excute_webcrawler3():
    webresult = []
    for i in url_trans():
        for j in get_time(i):
            webresult.append(j)

    print(webresult)


excute_webcrawler3()



