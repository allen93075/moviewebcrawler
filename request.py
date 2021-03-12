from bs4 import BeautifulSoup
import requests
import re
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


a = {
    'Name':"QQQQ",
    'time':"RRRRR"
}
print(a)

a["Name"] = 12345

print(a)