import json
from bs4 import BeautifulSoup
from types import SimpleNamespace
import ast
import os
import math
import csv
from select_found import *


def scrape_json():
    # open list of links
    # find the <script> tag
    # parse JSON and write to file
    
    data = []

    # read HTML pages
    for html in links_list:
        with open(html, 'r', encoding='utf-8', errors='ignore') as f_in:
            soup = BeautifulSoup(f_in.read(), 'html.parser')

        # find the script tag
        script_text = '//beware of injecting user-generated content'
        script = soup.find(lambda tag:tag.name=='script' and script_text in tag.text).text

        # clean JSON
        remove_before = '//beware of injecting user-generated content into the page here without sanitizing it \
            window.__PRELOADED_STATE__ = window.__PRELOADED_STATE__ || {}; \
            "window.__PRELOADED_STATE__.vintagePageInformation ='
        # remove_before = '//beware of injecting user-generated content into the page here without sanitizing it \
        #     window.__PRELOADED_STATE__ = window.__PRELOADED_STATE__ || {}; \
        #     "window.__PRELOADED_STATE__.offerPageInformation ='
        remove_after = "window.__PRELOADED_STATE__.merchantId = parseInt('') || null;"
        for rb in remove_before:
            script = script.replace(rb, '', 1)
        script = script.replace(remove_after, '')
        script = script.replace('{vintage"', '{"vintage"')
        script = script.replace('"is_deal_page":false};', '"is_deal_page":false}')
        script = script.replace('"global"', '"global_w"') # name "global" is inacceptable
        script = os.linesep.join([s for s in script.splitlines() if s]) # remove empty lines

        # parse JSON into an object with attributes corresponding to dict keys
        json_data = ast.literal_eval(json.dumps(script))
        try:
            j = json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))
        except:
            continue

        winery = j.vintage.wine.winery.name
        vintage = j.vintage.wine.name
        year = j.vintage.year
        region = j.vintage.wine.region.name

        rating = j.vintage.statistics.ratings_average
        ratings_count = j.vintage.statistics.ratings_count
        country_rank =  math.ceil(j.vintage.ranking.country.rank / j.vintage.ranking.country.total * 100)
        region_rank =  math.ceil(j.vintage.ranking.region.rank / j.vintage.ranking.region.total * 100)
        winery_rank =  math.ceil(j.vintage.ranking.winery.rank / j.vintage.ranking.winery.total * 100)
        # redwine_rank =  math.ceil(j.vintage.ranking.wine_type.rank / j.vintage.ranking.wine_type.total * 100)
        global_rank =  math.ceil(j.vintage.ranking.global_w.rank / j.vintage.ranking.global_w.total * 100)

        foods = []
        for food in  j.vintage.wine.foods:
            foods.append(food.name)
        
        try:
            alcohol = j.vintage.wine_facts.alcohol
        except:
            alcohol = None
        try:
            drink_from = j.vintage.wine_facts.drink_from
            drink_until = j.vintage.wine_facts.drink_until
        except:
            drink_from, drink_until = (None, None)
        try:
            style = j.vintage.wine.style.name
        except:
            style = None
        try:
            body = j.vintage.wine.style.body
        except:
            body = None
        try:
            body_desc = j.vintage.wine.style.body_description
        except:
            body_desc = None
        try:
            acidity = j.vintage.wine.style.acidity
        except:
            acidity = None
        try:
            acidity_desc = j.vintage.wine.style.acidity_description
        except:
            acidity_desc = None
        try:
            grapes = j.vintage.grapes[0].name
        except:
            grapes = None

        try:
            price = j.prices_and_availability.availability.median.amount
        except:
            try:
                price = j.prices_and_availability.availability.price.amount
            except:
                price = None

        try:
            highlights = []
            for highlight in  j.highlights:
                highlights.append(highlight.message)
            highlights_types = []
            for h_type in  j.highlights:
                highlights_types.append(h_type.highlight_type)
        except:
            highlights = None


        # append data to list
        data.append((winery, vintage, year, region, rating, ratings_count, \
                country_rank, region_rank, winery_rank, global_rank, \
                foods, alcohol, drink_from, drink_until, style, body, \
                body_desc, acidity, acidity_desc, grapes, price, highlights))


    # write data to CSV file
    columns = ['winery', 'vintage', 'year', 'region', 'rating', 'ratings_count', \
            'country_rank', 'region_rank', 'winery_rank', 'global_rank', \
            'foods', 'alcohol', 'drink_from', 'drink_until', 'style', 'body', \
            'body_desc', 'acidity', 'acidity_desc', 'grapes',  'price', 'highlights']

    file_name = 'data/spain-red.csv'
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        writer.writerow((columns))
        writer.writerows(data)
    

scrape_json()