import requests
import json
import csv


class AjaxScraper:
    results = []

    def fetch(self, url):
        return requests.get(url)
    
    def parse(self, content):
        self.results = content['data']
                
        for entry in self.results:
            del entry['_id']
    
    def to_csv(self):
        with open('table.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
    
    def run(self):
        response = self.fetch('https://scrapingkungfu.herokuapp.com/api?_=1576384789999')
        self.parse(response.json())
        self.to_csv()

if __name__ == '__main__':
    scraper = AjaxScraper()
    scraper.run()
