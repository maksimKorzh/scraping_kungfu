import requests
from bs4 import BeautifulSoup
import csv


class TableScraper:
    results = []

    def fetch(self, url):
        return requests.get(url)
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        table = content.find('table')
        rows = table.findAll('tr')
        self.results.append([header.text for header in rows[0].findAll('th')])
        
        for row in rows:
            if len(row.findAll('td')):
                self.results.append([data.text for data in row.findAll('td')])
    
    def to_csv(self):
        with open('table.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(self.results)
    
    def run(self):
        response = self.fetch('https://scrapingkungfu.herokuapp.com/chamber_5')
        self.parse(response.text)
        self.to_csv()

if __name__ == '__main__':
    scraper = TableScraper()
    scraper.run()
