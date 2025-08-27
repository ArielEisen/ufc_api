import requests
from bs4 import BeautifulSoup
from api import app, db, UFCChampModel

def web_scrape_champs(url, division):
    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')

    division_champs = soup.find_all('div', class_='field field--name-text field--type-text-long field--label-hidden field__item')

    
    
    
    with app.app_context():
        for i in range(len(division_champs)):
            former_champ_block = division_champs[i].find_all('p')
            for j in range(len(former_champ_block) ):
                if former_champ_block[j].text == 'Order UFC 309: Jones vs Miocic':
                    continue
                former_champ = former_champ_block[j].find('strong')
                if former_champ is None:
                    continue
                if 'RELATED:' in former_champ.text:
                    continue
                if 'View' in former_champ.text:
                    continue
                if 'MORE' in former_champ.text:
                    continue
                if 'Order' in former_champ.text:
                    continue
                if 'Career' in former_champ.text:
                    continue
                champ_split = former_champ.text.split(' ', 2)
                if len(champ_split) >= 3:
                    first_name = champ_split[0]
                    last_name = champ_split[1]
                    duration = champ_split[2]
                    current = 0
                else:
                    first_name = champ_split[0]
                    last_name = champ_split[1]
                    duration = None
                    current = 0

                
                champ = UFCChampModel(first_name=first_name, last_name=last_name, duration=duration, current=current, division=division)
                db.session.add(champ)
                db.session.commit()
                print(f"Inserted {first_name} {last_name} {duration} {division} {current}")


def main():
     with app.app_context():
        web_scrape_champs('https://www.ufc.com/news/ufc-flyweight-title-lineage-johnson-cejudo-figueiredo-moreno', 'flyweight')
        web_scrape_champs('https://www.ufc.com/news/ufc-bantamweight-title-lineage-cruz-dillashaw-garbrandt-cejudo-yan-sterling', 'bantamweight')
        champ = UFCChampModel(first_name='Merab', last_name='Dvalishvili', duration='(2024-Present)', current=1, division='bantamweight')
        db.session.add(champ)
        db.session.commit()

        web_scrape_champs('https://www.ufc.com/news/ufc-featherweight-title-lineage-aldo-mcgregor-holloway-volkanovski',  'featherweight')
        web_scrape_champs('https://www.ufc.com/news/ufc-lightweight-title-lineage-khabib-mcgregor-penn-poirier-oliveira', 'lightweight')
        web_scrape_champs('https://www.ufc.com/news/ufc-welterweight-title-lineage', 'welterweight')
        champ = UFCChampModel(first_name='Belal', last_name='Muhammad', duration='(2024-Present)', current=1, division='welterweight')
        db.session.add(champ)
        db.session.commit()
        web_scrape_champs('https://www.ufc.com/news/ufc-middleweight-title-lineage-adesanya-whittaker-GSP-bisping-silva-history', 'middleweight')
        web_scrape_champs('https://www.ufc.com/news/ufc-light-heavyweight-title-lineage-jones-cormier-blachowicz-teixeira-prochazka', 'light heavyweight')
        web_scrape_champs('https://www.ufc.com/news/ufc-heavyweight-title-lineage', 'heavyweight')


main()




