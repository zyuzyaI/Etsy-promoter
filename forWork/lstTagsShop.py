from selenium import webdriver
import time 
import datetime
from getProxyUSA import GetProxy
import csv
import os 

class SearchShop:
	def __init__(self, shop, tag, name):
		self.shop = shop 
		self.tag = tag 
		self.name = name
		self.worker()
		self.browser.close()

	def worker(self):
		proxy = '206.81.1.199:80' #GetProxy()
		firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True

		firefox_capabilities['proxy'] = {
			"proxyType": "MANUAL",
			"httpProxy": proxy,
			"ftpProxy": proxy,
			"sslProxy": proxy
			}

		self.browser = webdriver.Firefox(capabilities=firefox_capabilities)
		self.browser.get(f"https://www.etsy.com/search?q={self.tag}")
		self.make_scroll()
		self.get_pages()
		k = False
		for page in range(20): #range(self.total_pages)
			time.sleep(2)
			self.browser.get(f"https://www.etsy.com/search?q={self.tag}&ref=pagination&page={page+1}")
			items = self.browser.find_elements_by_css_selector('.wt-grid__item-xl-3')
			for i in range(len(items)):
				try:
					tmp_shop = items[i].find_element_by_class_name('text-gray-lighter').text 
				except:
					pass
				if tmp_shop == self.shop:
					try:
						self.title = items[i].find_element_by_tag_name('a').get_attribute('href')
					except:
						self.title = 'None'
					self.date = datetime.datetime.now().date()
					self.pos = page * 48 + i 
					self.page = page + 1
					print('saving...  ', end='')
					print(self.tag )
					self.save_csv()
					k = True
			if k:
				break
			if page == 19:
				print('Do something with this tag:  ', self.tag)
				with open(f'{self.name}.csv', 'a') as f:
					writer = csv.writer(f)
					writer.writerow(('Do something with this tag:  ', self.tag))


	def make_scroll(self):
		for i in range(3):
			self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(1)

	def save_csv(self):	
		url = self.title.split('/')[5]	
		with open(f'{self.name}.csv', 'a') as f:
				writer = csv.writer(f)
				writer.writerow((self.date, self.shop, self.tag, self.pos, self.page, self.total_pages))
		
	def get_pages(self):
		try:
			time.sleep(3)
			self.total_pages = int(self.browser.find_elements_by_css_selector('.wt-action-group__item')[-2].text.split('\n')[-1])
		except:
			print('No found')
			self.browser.close()
			print("do not found:  ", self.tag)
			self.total_pages = 1
			
	
if __name__ =='__main__':
	shop = 'MemoryFromPast'#input('Shop name:\n')
	tags = '+'.join(input("Search tag:\n").split())
	path = f"{os.getcwd()}/{shop}"
	id_title = '753427009'
	try: 
		os.mkdir(path) 
	except OSError as error: 
		pass   
	name = f"{path}/{id_title}"

	for tag in tags:
		SearchShop(shop, tag, name)