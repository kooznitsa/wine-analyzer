# Wine Scraper & Analyzer
1. Open Vivino.com.
2. Set the search parameters you need (e.g. Spanish red wines, all prices, all ratings).
3. Scroll to the end of the page with results to load all listings.
4. Manually download the web page and rename it (e.g. spain-red.html).
5. Use url_scraper.py to create a list of URLS.
6. Use page_downloader.py to download pages.
7. Use json.scraper.py to scrape JSON from downloaded pages.
Note that some vars (1986 scripts) are window.__PRELOADED_STATE__.vintagePageInformation,
and some (32 scripts) are window.__PRELOADED_STATE__.offerPageInformation.  
8. The result will be written to data/spain-red.csv.
9. Data analysis notebooks are in the notebooks folder.
