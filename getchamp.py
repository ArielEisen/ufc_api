import requests
from bs4 import BeautifulSoup

#getting html doc and instantiating with soup
html_doc = requests.get('https://www.ufc.com/athletes').text
soup = BeautifulSoup(html_doc, 'html.parser') 

champions = soup.find_all('div', class_='ath-n ath-lf-fl')

for i in range(0,8):
    champion = champions[i].find('span').find('span').text
    print(champion)

