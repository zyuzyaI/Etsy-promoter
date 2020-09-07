import requests
from bs4 import BeautifulSoup

from random import choice 

import ipinfo
import pprint

#proxy = {"http": "http://163.172.28.22:80"}

headers = {
    "Connection" : "close",  # another way to cover tracks
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

http_proxy  = "http://163.172.28.22:80"
#https_proxy = "https://163.172.28.22:80"

s = requests.Session()
s.proxies = http_proxy

ftp_proxy   = "ftp://163.172.28.22:80"

proxy = { 
              "http"  : http_proxy, 
              
              "ftp"   : ftp_proxy
            }

set_http_proxy=10.10.1.10:3128
set https_proxy=10.10.1.11:1080
set ftp_proxy=10.10.1.10:3128

r = s.get("https://www.expressvpn.com/ru/what-is-my-ip")#, proxies=proxy, headers=headers)
print(r)
soup = BeautifulSoup(r.text, 'lxml')
print(soup.find('div', class_='tool-panel__body').text)

# access_token = 'b8001b99619479'
# handler = ipinfo.getHandler(access_token)
# # ip_address = '178.128.52.156'
# details = handler.getDetails()
# pprint.pprint(details.all)


