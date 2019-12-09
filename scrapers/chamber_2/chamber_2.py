import requests
from bs4 import BeautifulSoup
import json
import csv


class ElementsScraper:
    results = []

    def fetch(self, url):
        return requests.get(url)
    
    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        
        titles = [title.text for title in content.findAll('strong', {'class': 'movie-title'})]
        genres = [genres.text for genres in content.findAll('span', {'class': 'movie-genre'})]
        countries = [countries.text for countries in content.findAll('span', {'class': 'movie-country'})]
        years = [years.text for years in content.findAll('span', {'class': 'movie-year'})]
        directors = [directors.text for directors in content.findAll('span', {'class': 'movie-director'})]
        starrings = [starrings.text for starrings in content.findAll('span', {'class': 'movie-starring'})]
        posters = [posters['src'] for posters in content.findAll('img', {'class': 'movie-poster'})]
        
        for index in range(0, len(titles)):
            self.results.append({
                'title': titles[index],
                'genre': genres[index],
                'country': countries[index],
                'year': years[index],
                'director': directors[index],
                'starring': starrings[index],
                'poster': posters[index]
            })
    
    def to_csv(self):
        with open('movies.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()
            
            for row in self.results:
                writer.writerow(row)
        
    def run(self):
        response = self.fetch('https://scrapingkungfu.herokuapp.com/chamber_2')
        self.parse(response.text)
        self.to_csv()


if __name__ == '__main__':
    scraper = ElementsScraper()
    scraper.run()
