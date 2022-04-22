from bs4 import BeautifulSoup
import re
from select_found import *


# 1. ATTN: exec() doesn't work inside functions
# 2. This code would work only with completely donwloaded web pages (with assets etc.)
# 3. Vivino.com doesn't allow Selenium
def read_html():
    # read HTML pages
    for html in links_list:
        with open(html, 'r', encoding='utf-8', errors='ignore') as f_in:
            soup = BeautifulSoup(f_in.read(), 'html.parser')


        def collect_wtastes():
            # collect wine tastes from HTML,
            # create a dictionary,
            # assign dict values to variables

            try:
                tastes_table = soup.find('table', attrs={'class':'tasteStructure__tasteStructure--15VDn'})
            except:
                continue
            if tastes_table:
                tastes_names = []
                tastes_values = []
                for taste in tastes_table:
                    taste_cells = taste.find_all('div', attrs={'class':'tasteStructure__property--loYWN'})
                    taste_indicators = taste.find_all('span', attrs={'class':'indicatorBar__progress--3aXLX'})
                    for tc in taste_cells:
                        tc = tc.text
                        tastes_names.append(tc)
                    for ti in taste_indicators:
                        ti = ti['style']
                        p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
                        if re.search(p, ti) is not None:
                            for catch in re.finditer(p, ti):
                                ti = catch[0]
                        tastes_values.append(ti)
                N = 2 # group list elements by twos
                tastes_names = [tastes_names[n:n+N] for n in range(0, len(tastes_names), N)]
                tastes_names = ['_'.join(i) for i in tastes_names]
                tastes_dict = {tastes_names[i]: tastes_values[i] for i in range(len(tastes_names))} # create dictionary
                # print(tastes_dict)
                # {'Light_Bold': '64.2307', 'Smooth_Tannic': '60.1248', 'Dry_Sweet': '7.68445', 'Soft_Acidic': '64.3765'}

                light_bold, smooth_tannic, dry_sweet, soft_acidic = (0,0,0,0)

                # convert strings to var names
                for k, v in tastes_dict.items():
                    exec("%s = %f" % (k.lower(), float(v))) # doesn't work inside function

            return light_bold, smooth_tannic, dry_sweet, soft_acidic


        def collect_wnotes():
            # collect wine notes from HTML,
            # create dictionaries,
            # assign dict values to variables

            try:
                notes_slider = soup.find('div', attrs={'class':'slider__slider--28TGJ slider__showControls--3JyG7 slider__grid--tKls1'})
            except:
                continue
            try:
                slides = notes_slider.find_all('button', attrs={'class':'card__card--2R5Wh tasteNote__tasteNote--1yWuX'})
            except:
                continue
            if slides:
                note_titles = []
                note_keywords = []
                note_mentions = []

                for slide in slides:
                    note_title = slide.find('title').text[:-5]
                    note_keyword = slide.find('div', attrs={'class':'tasteNote__popularKeywords--1q7RG'}).text
                    note_mention = slide.find('div', attrs={'class':'tasteNote__mentions--1Hjv0'}).text
                    note_titles.append(note_title)
                    note_keywords.append(note_keyword)
                    note_mentions.append(note_mention)

                # edit mentions
                edited_mentions = []
                for i in note_mentions:
                    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
                    if re.search(p, i) is not None:
                        for catch in re.finditer(p, i):
                            i = catch[0]
                            edited_mentions.append(i)
                    note_mentions = edited_mentions

                # create dictionaries
                notes_names_dict = {note_titles[i]: note_keywords[i] for i in range(len(note_titles))}
                notes_nums_dict = {note_titles[i]: note_mentions[i] for i in range(len(note_titles))}
                # print(notes_nums_dict)
                # {'oaky': '40', 'blackberries': '18', 'redberries': '17', 'earthy': '12', 'spices': '6', 
                # 'driedfruit': '2', 'treefruit': '2', 'vegetal': '1', 'yeasty': '1', 'citrus': '1'}

                oaky, blackberries, earthy, yeasty, spices, redberries, ageing, \
                    driedfruit, floral, vegetal, citrus, treefruit, tropical = (0,0,0,0,0,0,0,0,0,0,0,0,0)

                # convert strings to var names
                for k, v in notes_nums_dict.items():
                    exec("%s = %d" % (k, int(v))) # doesn't work inside function
        
            return  notes_names_dict, oaky, blackberries, earthy, yeasty, spices, redberries, ageing, \
                        driedfruit, floral, vegetal, citrus, treefruit, tropical

    return collect_wtastes(), collect_wnotes()