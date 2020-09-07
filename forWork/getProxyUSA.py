"""This class return proxy from USA in this format ==> http://159.138.22.112:80"""
from selenium import webdriver
from random import choice

class GetProxy:
	# when you need return some variable you need work with __new__
	def __new__(cls):
		
		url = 'http://www.gatherproxy.com/proxylist/country/?c=United%20States'
		browser = webdriver.Firefox()
		browser.get(url)

		hosts = [i.text.strip() for i in browser.find_elements_by_css_selector('td:nth-child(2)')]
		ports = [i.text.strip() for i in browser.find_elements_by_css_selector('td:nth-child(3) a')]
		
		lst = [f"{hosts[i]}:{ports[i]}" for i in range(len(hosts))]

		browser.close()

		proxy = choice(lst)

		return str(proxy)

if __name__ == '__main__':
	k = GetProxy()
	print(k)
