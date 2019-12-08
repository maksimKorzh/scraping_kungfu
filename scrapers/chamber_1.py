import requests
from bs4 import BeautifulSoup
import json


class ItemScraper:
    def fetch(self, url):
        return requests.get(url)
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        title = content.find('h4').text
        container = content.find('div', {'class': 'col-md-9'})
        items = [item.text.replace('\n', '') for item in container.findAll('p')]
        genre = ''.join([item.split(':')[-1] for item in items if 'Genre' in item])
        country = ''.join([item.split(':')[-1] for item in items if 'Country' in item])
        year = ''.join([item.split(':')[-1] for item in items if 'Year' in item])        
        director = ''.join([item.split(':')[-1] for item in items if 'Director' in item]).strip()
        starring = ''.join([item.split(':')[-1] for item in items if 'Starring' in item]).strip()
                
        scraped_item = {
            'title': title,
            'genre': genre,
            'country': country,
            'year': year,
            'director': director,
            'starring': starring
        }
        
        print(json.dumps(scraped_item, indent=2))
    
    def run(self):
        response = self.fetch('https://scrapingkungfu.herokuapp.com/chamber_1')
        self.parse(response.text)


if __name__ == '__main__':
    scraper = ItemScraper()
    scraper.run()
