FROM python:3.8
RUN pip install pipenv
COPY . /tmp/myapp
RUN cd /tmp/myapp && pipenv lock --keep-outdated --requirements > requirements.txt
RUN pip install -r /tmp/myapp/requirements.txt
WORKDIR /tmp/myapp
CMD sleep 60 && scrapy crawl covid -a state_path=/tmp/covidstate/state.json