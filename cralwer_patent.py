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

def next_month(date):
	if (int(date / 100) % 100 == 12):
		return (date - 1100 + 10000)
	else:
		return (date + 100)

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
	begin_date = 20170101
	end_date = 20170901
	curr_date = begin_date
	domain_url = "https://patents.google.com"
	
	start_url = domain_url + "/?assignee=" + search_word + "&before=filing:" + str(next_month(begin_date)) \
		+ "&after=" + str(begin_date) + "&num=100"
	driver.get(start_url)

	# Wait for manually applying filter (if needed)
	time.sleep(5)

	# Read in previous result
	output_file = "patents.json"
	try:
		with open(output_file) as f:
			patent_result = json.load(f)
	except:
		patent_result = []


	while(curr_date != end_date):

		start_url = domain_url + "/?assignee=" + search_word + "&before=filing:" + str(next_month(curr_date)) \
		+ "&after=" + str(curr_date) + "&num=100"
		driver.get(start_url)

		has_next = True
		page_num = 0

		while(has_next):

			locator = (By.XPATH, "//article[@class='result style-scope search-result-item']")
			if not wait_to_load(driver, locator):
				break
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

				# TODO
				next_url = domain_url + "/?assignee=" + search_word + "&before=filing:" + str(next_month(curr_date)) \
					+ "&after=" + str(curr_date) + "&page=" + str(page_num) + "&num=100"
				driver.get(next_url)

				# TODO: Can only see 300 results from Google Patents
				if page_num > 2:
					has_next = False
			except:
				has_next = False

			print('Success Collect ' + str(page_num) + " pages!")

		curr_date = next_month(curr_date)


	open(output_file, 'w').close()
	print_to_file(output_file, json.dumps(patent_result))


if __name__ == '__main__':
	main()


