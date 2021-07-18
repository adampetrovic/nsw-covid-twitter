FROM python:3.8
RUN pip install pipenv
COPY . /tmp/myapp
RUN cd /tmp/myapp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/myapp/requirements.txt
WORKDIR /tmp/myapp
CMD scrapy crawl covid --loglevel WARNING && sleep 60