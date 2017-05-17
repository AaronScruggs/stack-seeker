import requests
from bs4 import BeautifulSoup
import csv
from global_variables import proxy_list, request_headers
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
import re
from stack_scraper import StackScraper


class BusinessListingScraper:
    def __init__(self,
                 base_url='http://www.manta.com/mb_53_G2_CKV',
                 term='computer_software',
                 region='las_vegas_nv',
                 first_page=1,
                 stop_page=2):
        self.base_url = base_url
        self.term = term
        self.region = region
        self.start_page = first_page
        self.stop_page = stop_page
        self.driver = None
        self.weblink_constant = '/api/v1/urlverify/http%3A%2F%2F'

    def init_selenium_scraper(self):
        myProxy = '119.237.211.19'
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", myProxy)
        profile.set_preference("network.proxy.http_port", 3128)
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile)
        self.driver = driver

    def request_html(self, page_num):
        url = '/'.join([self.base_url, self.term, self.region]) + '?pg={}'.format(page_num)
        self.driver.get(url)
        return self.driver.page_source


    def get_website_list(self, content):
        # Take manta html content and return a list of business websites
        soup = BeautifulSoup(content, 'html.parser')
        hrefs = soup.find_all('a', href=re.compile(self.weblink_constant))
        links = [x['href'].strip(self.weblink_constant) for x in hrefs]
        return list(set(links))

    def lookup_website_list(self, website_list):
        pass


    def process_companies(self):
        # for each page: get html from manta, get list of business urls, run stack scraper on each

        self.init_selenium_scraper()
        for page_num in range(self.start_page, self.stop_page):
            html = self.request_html(page_num)
            if html:
                website_list = self.get_website_list(html)
                self.lookup_website_list(website_list)
