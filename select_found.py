import os
import glob
from bs4 import BeautifulSoup

found_scripts = []
not_found_scripts = []

def select_found():
    folder = 'web-pages/spain-red/www.vivino.com/NL/en'
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
    for wine_name in sub_folders:
        html_files = glob.glob(f'web-pages\\spain-red\\www.vivino.com\\NL\\en\\{wine_name}\\w\\*.html')
        for html in html_files:

            with open(html, 'r', encoding='utf-8', errors='ignore') as f_in:
                soup = BeautifulSoup(f_in.read(), 'html.parser')

            try:
                script_text = '//beware of injecting user-generated content'
                script = soup.find(lambda tag:tag.name=='script' and script_text in tag.text).text
                found_scripts.append(html)
            except:
                not_found_scripts.append(html)
                continue

select_found()

print('NOT FOUND: ', len(not_found_scripts))
links_list = [x for x in found_scripts if x not in not_found_scripts]
print('ULTIMATE LIST LENGTH: ', len(links_list))