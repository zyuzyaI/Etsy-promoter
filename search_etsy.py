# for change IP
from fake_useragent import UserAgent
import socks
import socket
from bs4 import BeautifulSoup
#for get html
import requests
import time
#save in csv
import csv

def save_csv(page, item_url):
	with open(f'data.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerow((item_url.split('/')[5].split('?')[0].replace('-', ' '), page, item_url))

def change_ip():
	socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
	socket.socket = socks.socksocket
	ip = requests.get('http://checkip.dyndns.org').content
	soup = BeautifulSoup(ip, 'html.parser')
	print(soup.find('body').text)

def get_html(url):
	html = requests.get(url, headers={'User-Agent': UserAgent().chrome})
	print(html)
	return html

def get_bs(html):
	soup = BeautifulSoup(html.text, 'lxml')
	return soup

def search_item(html, your_shop):
	print('searching...')
	urls = []
	soup = get_bs(html)
	try:
		url_shop = soup.find('ul', class_='responsive-listing-grid wt-grid wt-grid--block justify-content-flex-start pl-xs-0')
		for i in url_shop:
			try:
				shop_name = i.find('p', class_='text-gray-lighter text-body-smaller display-inline-block').text
				if your_shop in shop_name:
					my_url = i.find('div', class_='js-merch-stash-check-listing v2-listing-card position-relative flex-xs-none').find('a')
					my_url = my_url['href']
					urls.append(my_url)
			except:
				pass
	except:
		return urls
	return urls

def go_to(urls, counter):
	for i in urls:
		print(f'get request...\n(page = {counter})')
		html = get_html(i)
		save_csv(counter, i)
		time.sleep(5)

def total_pages(url):
	html = get_html(url)
	soup = get_bs(html)
	try:
		pages = soup.find('div', class_='mb-xs-5 mt-xs-3').find_all('a', class_='wt-btn wt-btn--small wt-action-group__item')
		page = int(pages[-1]['href'].strip().split('=')[-1])
		print(f"pages => {page}")
	except:
		page = 1
	return page

def word_search():
	input_word = input('Please write what you want to find:\n')
	try:
		words = '+'.join(input_word.split())
		return words
	except:
		print('Error, try again')
		word_search()

def your_shop_name():
	return input('Input name of yor shop:\n')

def main():
	main_words = word_search()
	url_s = ('https://www.etsy.com/search?q=' + main_words + '&ref=pagination&page=1')
	your_shop = your_shop_name()
	for i in range(1,total_pages(url_s)+1):
		change_ip()
		url = (url_s + str(i))
		html = get_html(url)
		my_url = search_item(html, your_shop)
		if my_url:
			go_to(my_url,i)
		time.sleep(11)

if __name__ == '__main__':
	main()
