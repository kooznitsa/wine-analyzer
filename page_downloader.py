# https://pypi.org/project/pywebcopy/
from pywebcopy import WebPage, config
import csv

file_path = 'data/links.csv'

project_folder = 'web-pages'
project_name = 'wine-pages'
kwargs = {'bypass_robots': True}

with open(file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    for url in reader:
        url = ''.join(map(str, url))

        # You should always start with setting up the config or use apis
        config.setup_config(url, project_folder, project_name, **kwargs)

        # Create a instance of the webpage object
        wp = WebPage()

        # If you want to use `requests` to fetch the page then
        wp.get(url)

        # Else if you want to use plain html or urllib then use
        # wp.set_source(object_which_have_a_read_method, encoding='utf-8')
        # you need to do this if you are using set_source()
        # wp.url = url

        # Then you can access several methods like
        # wp.save_complete()
        wp.save_html()
        # wp.save_assets()