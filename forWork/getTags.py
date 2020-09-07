from selenium import webdriver
from getProxyUSA import GetProxy
import time

class GetTags:
	def __init__(self, keys):
		self.keys = keys 
		self.maker()

	def maker(self):
		proxy = GetProxy()
		firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
		firefox_capabilities['marionette'] = True

		firefox_capabilities['proxy'] = {
			"proxyType": "MANUAL",
			"httpProxy": proxy,
			"ftpProxy": proxy,
			"sslProxy": proxy
			}

		browser = webdriver.Firefox(capabilities=firefox_capabilities)
		browser.get('https://www.etsy.com/')
		time.sleep(2)
		url = f"https://www.etsy.com/search?q={self.keys}"
		browser.get(url)
		pages = browser.find_elements_by_css_selector('.wt-action-group__item')[-2].text.split('\n')[-1]
		name = f"{self.keys}_page-{pages}"
		pattr = browser.find_elements_by_css_selector('.wt-grid__item-xl-3')
		urls = [i.find_element_by_tag_name("a").get_attribute('href') for i in pattr] 

		tag_lst =[]
		for url in urls:
			browser.get(url)
			time.sleep(2)
			tags = browser.find_elements_by_css_selector('.wt-mr-xs-1 .btn-secondary')
			[tag_lst.append(i.text + '\n') for i in tags]

		set_tag = set(tag_lst)
		with open(f"{name}.txt", 'a+', encoding='utf8') as f:
			for i in set_tag:
				f.write(i + '\n')

		browser.close()

class InputKey:
	def __new__(self):
		while True:
			try:
				search = input("Введіть слова пошуку:\n")
				lst = search.split()
				lst = '+'.join(lst)
				return lst
			except:
				print('Щось не так!!!!')
				
 

if __name__ == '__main__':
	keys = InputKey()
	GetTags(keys) 