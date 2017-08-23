from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
import json
import requests
import re
import time


def print_to_file(filename, data):
	with open(filename, 'a') as f:
		f.write(data)


def wait_to_load(driver, locator):
	try:
		WebDriverWait(driver, 20).until(
			EC.presence_of_element_located(locator)
		)
		return 1
	except:
		print(locator)
		print('Fail to load!')
		return 0

def main():

	# Webdriver Setting
	# dcap = dict(DesiredCapabilities.PHANTOMJS)
	# headers = {'Referer':'https://aminer.org/', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	# for key, value in headers.items():
	# 	dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
	# dcap['phantomjs.page.settings.userAgent'] = \
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
	# dcap['phantomjs.page.settings.loadImages'] = False
	
	# service_args = ['--proxy=205.189.37.79:53281', '--proxy-type=none']
	driver = webdriver.Firefox()
	# driver = webdriver.PhantomJS(desired_capabilities=dcap)

	# When using phantomjs, need to maximize the window
	driver.maximize_window()

	# Check IP
	# check_url = "http://www.whatismyip.org"
	# driver.get(check_url)
	# locator = (By.XPATH, "/html/body/div[2]/span")
	# wait_to_load(driver, locator)
	# IP = driver.find_element(By.XPATH, "/html/body/div[2]/span")
	# print(IP.text)

	search_word = "Denso+Corporation"
	domain_url = "https://patents.google.com"
	start_url = domain_url + "/?assignee=" + search_word + "&num=100"
	driver.get(start_url)

	time.sleep(10)

	patent_result = []
	has_next = True
	page_num = 0

	output_file = "patents.json"
	open(output_file, 'w').close()

	while(has_next):

		locator = (By.XPATH, "//article[@class='result style-scope search-result-item']")
		wait_to_load(driver, locator)
		patent_lists = driver.find_elements(By.XPATH, "//article[@class='result style-scope search-result-item']")

		for patent in patent_lists:
			patent_item = {}
			title = patent.find_elements(By.ID, "htmlContent")[0].text
			url = patent.find_element(By.ID, "link").get_attribute("href")
			snippet = patent.find_elements(By.ID, "htmlContent")[3].text
			# print(title)
			# print(url)
			# print(snippet)
			
			patent_item['title'] = title
			patent_item['url'] = url
			patent_item['snippet'] = snippet
			patent_result.append(patent_item)

		# Get Next Page
		try:
			page_num = page_num + 1
			next_url = domain_url + "/?assignee=" + search_word + "&page=" + str(page_num) + "&num=100"
			driver.get(next_url)
			if page_num > 2:
				has_next = False
		except:
			has_next = False

		print('Success Collect ' + str(page_num) + " pages!")


	print_to_file(output_file, json.dumps(patent_result))


if __name__ == '__main__':
	main()


