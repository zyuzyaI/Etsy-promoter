from fake_useragent import UserAgent
import socks
import socket
import requests
import time 
from bs4 import BeautifulSoup
import random

UserAgent().chrome

url = ["<urls list>"]

while True:
	url1 = random.choice(url)

	response = requests.get(url1, headers={'User-Agent': UserAgent().chrome})
	print(response)
	socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
	socket.socket = socks.socksocket
	ip = requests.get('http://checkip.dyndns.org').content
	soup = BeautifulSoup(ip, 'html.parser')
	print(soup.find('body').text)

	time.sleep(random.choice(range(60)))









