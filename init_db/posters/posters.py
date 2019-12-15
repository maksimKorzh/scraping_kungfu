import requests
from bs4 import BeautifulSoup
import time

class ImageDownloader:
    def fetch(self, url):
        return requests.get(url)
    
    def parse(self, json):
        return [image['poster'] for image in json['data']]

    def download(self, url):
        response = requests.get(url)
        filename = url.split('/foto/')[-1]
        
        print('Downloading image: %s from URL: %s' % (filename, url))
        
        if response.status_code == 200:
            with open('./images/' + filename, 'wb') as image_file:
                for chunk in response.iter_content(chunk_size=128):
                    image_file.write(chunk)
    
    def run(self):
        response = self.fetch('https://scrapingkungfu.herokuapp.com/api')
        images = self.parse(response.json())

        for image in images:
            self.download(image)
            #time.sleep(2)

if __name__ == '__main__':
    scraper = ImageDownloader()
    scraper.run()
