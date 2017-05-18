from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import re
from stack_scraper import StackScraper
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('info_logs.log')
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class BusinessListingScraper:
    def __init__(self,
                 url,
                 tech_term='django'):
        self.driver = None
        self.url = url
        self.weblink_constant = '/api/v1/urlverify/http%3A%2F%2F'
        self.tech_term = tech_term

    def init_selenium_scraper(self):
        myProxy = '119.237.211.19'
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", myProxy)
        profile.set_preference("network.proxy.http_port", 3128)
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile)
        # driver.set_page_load_timeout(5)
        self.driver = driver

    # def request_html(self, page_num):
    #     url = '/'.join([self.base_url, self.term, self.region]) + '?pg={}'.format(page_num)
    #     self.driver.get(url)
    #     print('title: ', self.driver.title)
        # return self.driver.page_source


    def lookup_website_list(self, website_list):
        for website in website_list:
            stack_scraper = StackScraper(self.tech_term, website, self.driver)
            stack_scraper.run_scrape()

    def connect_to_site(self):
        self.init_selenium_scraper()
        self.driver.get(self.url)

    def get_website_list(self):
        # Take manta html content and return a list of business websites
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        hrefs = soup.find_all('a', href=re.compile(self.weblink_constant))
        links = [x['href'].strip(self.weblink_constant) for x in hrefs]
        print(len(links), links)
        return list(set(links))

    def process_page(self):
        self.init_selenium_scraper()
        for i in range(4):
            try:
                self.driver.get(self.url)
            except TimeoutException:
                print('timed out')

            time.sleep(5)
            website_list = self.get_website_list()
            print(website_list)

            if website_list:
                self.lookup_website_list(website_list)
                break
            elif i==3:
                logger.info('missed: {}'.format(url))
            else:
                continue
        self.driver.quit()




if __name__ == '__main__':
    urls = ['http://www.manta.com/mb_53_A0_CKV/advertising_and_marketing/las_vegas_nv?pg={}'.format(x)
            for x in range(1, 20)]

    for url in urls:
        print(url)
        bls = BusinessListingScraper(url)
        bls.process_page()
