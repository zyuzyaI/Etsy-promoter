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

def main():
	main_words = word_search()
	url_s = ('https://www.etsy.com/search?q=' + main_words + '&ref=pagination&page=1')
	print(total_pages(url_s)+1))

if __name__ == '__main__':
	main()
