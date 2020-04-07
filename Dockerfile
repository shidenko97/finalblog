FROM python:3.8.1

MAINTAINER Serhii Hidenko "shidenko97@gmail.com"

RUN mkdir -p /www/finalblog
WORKDIR /www/finalblog

ADD requirements.txt /www/finalblog/
RUN pip install -r requirements.txt

ADD . /www/finalblog

CMD flask db upgrade && flask run --host 0.0.0.0 --port 5000