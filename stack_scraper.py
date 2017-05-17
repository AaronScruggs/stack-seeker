import requests
from bs4 import BeautifulSoup
import csv
from global_variables import proxy_list, request_headers


class StackScraper:
    """
    Search a companies website stack for the given search term. Positive results are written to the record file.
    """
    def __init__(self, tech_term, company_website, record_file='matching_companies.csv'):
        self.tech_term = tech_term.lower()
        self.base_url = 'https://builtwith.com/'
        self.company_website = company_website
        self.record_file = record_file

    def request_html(self):
        url = self.base_url + self.company_website
        for proxy in proxy_list:
            r = requests.get(url, proxies=proxy, headers=request_headers)
            if r.status_code == 200:
                return r
        return None

    def search_content(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find_all('div', class_='techItem')
        for item in items:
            lower_text = item.text.lower()
            if self.tech_term in lower_text:
                return self.tech_term
        return False

    def run_scrape(self):
        r = self.request_html()
        if r:
            result = self.search_content(r.content)
        else:
            result = 'Connection failed'

        with open(self.record_file, 'a') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow([self.company_website, result])

