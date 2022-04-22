# type of URL to parse
# <a class="_3qc2M wineCard__cardLink--3F_uB" data-testid="vintagePageLink" 
# href="/vega-sicilia-unico/w/77137?year=2009&amp;price_id=21057503">

from bs4 import BeautifulSoup
import csv
import pandas as pd

filepath = "web-pages/spain-red.html"
with open(filepath, 'r', encoding='utf-8', errors='ignore') as f_in:
    soup = BeautifulSoup(f_in.read(), 'html.parser')

# collect href links from HTML
links_list = []
links = soup.find_all('a', attrs = {'class' : '_3qc2M wineCard__cardLink--3F_uB'})
for link in links:
    links_list.append(link['href'])

# write links to a file
file_name = 'data/links.csv'
with open(file_name, 'w', encoding='utf-8', errors='ignore') as csv_file:
    for link in links_list:
        write = csv.writer(csv_file, lineterminator='\n')
        write.writerow([link])

# remove duplicated values
data = pd.read_csv(file_name)
data.drop_duplicates(keep='first', inplace=True)
data.to_csv(file_name, index=False)