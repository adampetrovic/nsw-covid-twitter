# nsw-covid-twitter
A twitter bot for tweeting about NSW exposure venues


- The logic for scraping from the Data NSW feed is in [covid.py](nswcovidbot/spiders/covid.py)
- The logic for sending it to twitter is a scrapy pipeline in `pipelines.py`
