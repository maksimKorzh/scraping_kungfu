import requests
import json
import csv
import time


class InfiniteScrollScraper:
    results = []

    def fetch(self, url, params):
        print('HTTP POST request to URL: %s' % url, end='')
        response = requests.post(url, params=params)
        print(' | Status code: %s' % response.status_code)
        
        return response
    
    def parse(self, content):
        data = content['data']
        
        for entry in data:
            self.results.append(entry)
    
    def to_csv(self):
        with open('res.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
            
            print('Strored data in "res.csv" file')
    
    def run(self):
        params = {
            'index': 0,
            'limit': 10
        }
        
        for page in range(0, 10):
            response = self.fetch('http://scrapingkungfu.herokuapp.com/api', params)
            self.parse(response.json())
            params['index'] += 10
            time.sleep(2)
        
        self.to_csv()


if __name__ == '__main__':
    scraper = InfiniteScrollScraper()
    scraper.run()
