# nsw-covid-twitter
A twitter bot for tweeting about NSW exposure venues


- The logic for scraping from the Data NSW feed is in [covid.py](nswcovidbot/spiders/covid.py)
- The logic for saving venues to a database and sending it to twitter is a scrapy pipeline in [pipelines.py](nswcovidbot/pipelines.py)

## Basic Data Flow:

1. Scrape the data from Data NSW's COVID-19 venue API
2. Pass each individual venue down the Scrapy Pipeline's (SQLPipeline & TwitterPipeline)
3. Check the database to see if the venue has been seen before. If not, save it to the database. Allow the item to pass through the pipeline.
4. If venue has already been seen, drop it from the pipeline (don't let it pass through)
5. Once we've finished scraping and all new venues have been saved, activate the `TwitterPipeline`
6. Check the database for any venues that don't have an associated Tweet.
7. Collate the new venues by venue name (one tweet per venue with multiple times)
8. Tweet the aggregate tweet and reply to this tweet with each venue
9. Save tweets against the venue record in the database.


## How to run the bot:
1. Ensure python3.8 is installed.
2. Install pipenv. `pip install pipenv`
3. `pipenv install` from the root of the repo
4. Activate the virtualenv with `pipenv shell`
5. Set the required environment variables in [settings.py](nswcovidbot/settings.py)
7. Run `scrapy crawl covid`
