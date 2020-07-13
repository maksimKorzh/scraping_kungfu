import requests
html = requests.get('http://quotes.toscrape.com/').text

def parse(html, query):
    for card in html.split(query):
        raw = card.split('</div>')[0]
        
        try:
            print(raw.split('small class="tag"')[1])
        
        except:
            pass
        
        


parse(
    html,
    '<div class="quote" itemscope itemtype="http://schema.org/CreativeWork">'
)

