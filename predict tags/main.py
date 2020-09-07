"""
You need to input listing url. Found tag position on Etsy shop. Created csv file with shop name, item title, tag, position, 
total page, visits predict, list of different  tags to change.
Proxy from USA. Ahd list of different users agents.
"""
import requests
from multiprocessing import Process
from bs4 import BeautifulSoup
from multiprocessing import Pool
import os
from random import choice
import csv
import multiprocessing
import multiprocessing.pool
import math
import random


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

# We sub-class multiprocessing.pool.Pool instead of multiprocessing.Pool
# because the latter is only a wrapper function, not a proper class.
class MyPool(multiprocessing.pool.Pool):
    Process = NoDaemonProcess

class TagList:
	def __init__(self, url):
		self.url = url
		self.worker()


	def worker(self):
		
		html = requests.get(self.url)
		soup = BeautifulSoup(html.text, 'lxml')

		self.id = soup.find('div', id='listing-right-column').find('h1').attrs['data-listing-id']
		self.title = soup.find('div', class_='listing-page-title-component').text.strip()
		self.shop_name = soup.find('div', class_='display-flex-xs align-items-center mb-xs-1').text.strip().split('\n')[0]
		body = soup.find('div', class_='col-xs-12 pl-xs-0 pr-xs-0 seller-tags-experiment').findAll('li')
		
		tags = [i.text.strip() for i in body]

		self.predict = [f"https://www.etsy.com/search?q={tag}" for tag in tags[:3]]

		p2 = MyPool(3)  # Pool tells how many at a time
		records2 = p2.map(PredTags, self.predict)
		p2.terminate()
		p2.close()
		p2.join()

		self.tmp_worker = []		
		extract_records = [records2[v].worker() for v in range(len(records2))]
		
		for item in extract_records:
			try:
				self.tmp_worker += item
			except:
				pass
		
		url_tags = [f"https://www.etsy.com/search?q={tag}" for tag in tags[3:]]
		
		n_tags = len(url_tags)
		print(n_tags)
		p = MyPool(n_tags)  # Pool tells how many at a time
		records = p.map(self.posTags, url_tags)
		p.terminate()
		p.close()
		p.join()
		
		print('work with posTags done!')

		

		
	def posTags(self, url):
		tmp = False
		user_agent = GetUA()
		proxy = GetProxy()
		tag = url.split('=')[-1]

		self.get_pages(url)			
		if self.total_pages > 30:
			self.pages = 30
		else:
			self.pages = self.total_pages

		for page in range(self.pages):
				url_tags = f"{url}&ref=pagination&page={page+1}"
				html_tags = requests.get(url_tags, {'User-Agent': user_agent}, proxies=proxy)
				soup_tags = BeautifulSoup(html_tags.text, 'lxml')
				pos_tag = soup_tags.find('ul', class_='responsive-listing-grid wt-grid wt-grid--block justify-content-flex-start pl-xs-0').find_all('li')
				for pos in range(len(pos_tag)):
					shop = pos_tag[pos].find('p', class_='text-gray-lighter text-body-smaller display-inline-block').text
					item_title = pos_tag[pos].find('h2', class_='text-gray').text.strip()
					if shop == self.shop_name  and self.title == item_title:
						items = {}
						items['title'] = item_title
						items['shop'] = shop 
						items['tag'] = tag 
						items['total_page'] = self.total_pages
						items['pos'] = page * 48 + pos
						items['predict'] = math.e**(-(page * 48 + pos)/128)*(
											self.total_pages/250)
						if math.e**(-(page * 48 + pos)/128)*(
											self.total_pages/250) < 0.02:
							self.random_tag()
							items['random_tags'] = self.pred_tags
						else:
							items['random_tags'] = None
						tmp = True
						self.save_csv(items)
						break 
				
				if tmp:
						break

				if page == 29:
					items = {}
					items['title'] = self.title
					items['shop'] = self.shop_name
					items['tag'] = f"{tag}"
					items['total_page'] = self.total_pages
					items['pos'] = None
					items['predict'] = 0
					self.random_tag()
					items['random_tags'] = self.pred_tags
					self.save_csv(items)
			
					

	def random_tag(self):
		
			self.pred_tags = random.sample(self.tmp_worker,5)

	def save_csv(self, items):
		print('saving....')
		print(self.id)
		name = f"template/{self.id}"
		try:
			# Create target Directory
			os.mkdir(name)
			print("Directory " , name,  " Created ") 
		except FileExistsError:
			print("Directory " , name,  " already exists")
		fullname = f"{os.getcwd()}/{name}"
		with open(f'{fullname}/{self.id}.csv', 'a', encoding="utf-8") as f:
			writer = csv.writer(f)
			writer.writerow((items['shop'],
							items['title'],
							items['tag'],
							items['pos'],
							items['total_page'],
							items['predict'],
							items['random_tags']															
						))
	
		
	def get_pages(self, url):
		html = requests.get(url)
		soup = BeautifulSoup(html.text, 'lxml')
		pages_soup = soup.find_all('li', class_='wt-action-group__item-container')
		self.total_pages = int(pages_soup[-2].text.strip().split('\n')[-1].strip())



class GetProxy:
	def __new__(self):
		html = requests.get('https://www.us-proxy.org/')
		soup = BeautifulSoup(html.text, 'lxml')
		trs = soup.find('table', id='proxylisttable').find('tbody').find_all('tr')
		lst = [f"{t.text}" for tr in trs for t in tr]
		proxies = [f"{lst[i]}:{lst[i+1]}" for i in range(0, 1600, 8)]
		while True:
			proxy = {"http": f"http://{choice(proxies)}"}
			r = requests.get('https://www.us-proxy.org/',  proxies=proxy)
			if r.status_code == 200:
				return proxy

class GetUA:
	def __new__(self):
		ua = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
			'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0',
			'Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0',
			'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0',
			'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
			'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0',
			'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
			'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
			'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
			'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0',
			'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:25.0) Gecko/20100101 Firefox/25.0',
			'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0',
			'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0',
			'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
			'Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36',
			'Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36',
			'Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36',
			'Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36',
			'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254',
			'Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1',
			'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1',
			'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15',
			'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1',
			'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
			'Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3',]
		return choice(ua)

class PredTags:
	def __init__(self, url):
		self.url = url 
			
	def worker(self):
		html = requests.get(self.url)
		soup = BeautifulSoup(html.text, 'lxml')

		row_urls = soup.find('ul', class_='responsive-listing-grid wt-grid wt-grid--block justify-content-flex-start pl-xs-0').find_all('li')

		lst_urls = [url.find('a').attrs['href'] for url in row_urls]

		p = Pool(12)  # Pool tells how many at a time
		records = p.map(Worker, lst_urls)
		p.terminate()
		p.join()
		
		tmp_worker = []		
		extract_records = [records[v].worker() for v in range(len(records))]
		
		for item in extract_records:
			try:
				tmp_worker += item
			except:
				pass
		
		lst_tmp = list(set(tmp_worker))
		pred_tsgs = sorted(lst_tmp, key=lambda k : tmp_worker.index(k))
			
		return pred_tsgs[:25]

class Worker:
	def __init__(self, url):
		self.url = url
						
	def worker(self):
		try:
			user_agent = GetUA()
			proxy = GetProxy()
			html = requests.get(self.url, {'User-Agent': user_agent}, proxies=proxy)
			if html.status_code == 200:
				soup = BeautifulSoup(html.text, 'lxml')
				self.title = soup.find('div', class_='listing-page-title-component').text.strip()
				self.shop_name = soup.find('div', class_='display-flex-xs align-items-center mb-xs-1').text.strip().split('\n')[0]
				body = soup.find('div', class_='col-xs-12 pl-xs-0 pr-xs-0 seller-tags-experiment').findAll('li')
				
				tags = [i.text.strip() for i in body]
				for tag in tags[3:]:
					return tags
					"""fullname = f"{os.getcwd()}/template"
					with open(f'{fullname}/tags_{self.name}.csv', 'a', encoding="utf-8") as f:
					writer = csv.writer(f)
					writer.writerow((tag,))"""
			else:
				return ['None']
		except:
			return ['None']


if __name__ == '__main__':
	while True:

		url = input("\n\t\t\tInput your listing url:\n\
(exmp:'https://www.etsy.com/listing/755650625/vintage-eyeglasses-glasses-for-women')\n\
                         if you want wait input 'y'\n\
============================================================================\n")
		if url.lower().strip() == 'y':
			break
		else:
			TagList(url)
	