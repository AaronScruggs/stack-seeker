import requests
from bs4 import BeautifulSoup
import csv
from global_variables import proxy_list, request_headers
import time


class StackScraper:
    """
    Search a companies website stack for the given search term. Positive results are written to the record file.
    """
    def __init__(self, tech_term, company_website, driver, record_file='matching_companies.csv'):
        self.tech_term = tech_term.lower()
        self.base_url = 'https://builtwith.com/'
        self.company_website = company_website
        self.record_file = record_file
        self.driver = driver
        self.url = self.base_url + self.company_website

    def request_html(self):
        url = self.base_url + self.company_website
        for proxy in proxy_list:
            r = requests.get(url, proxies=proxy, headers=request_headers)
            if r.status_code == 200:
                return r
        return None

    def check_term(self, items):
        for item in items:
            if self.tech_term in item:
                return True
        return False

    def search_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find_all('div', class_='techItem')
        text_items = [item.find('h3').text.lower() for item in items]
        return text_items


    def run_scrape(self):
        # r = self.request_html()
        self.driver.get(self.url)
        time.sleep(5)
        results = self.search_content(self.driver.page_source)
        term_found = self.check_term(results)
        results = [term_found] + results

        with open(self.record_file, 'a') as file:
            csvwriter = csv.writer(file)
            data = [self.company_website] + results
            csvwriter.writerow(data)
