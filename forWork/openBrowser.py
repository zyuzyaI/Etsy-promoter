from selenium import webdriver
from getProxyUSA import GetProxy 

class OpenBrowser:
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
	browser.get('https://www.etsy.com')


if __name__ == '__main__':
	OpenBrowser() 