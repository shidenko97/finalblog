FROM python:3.8.1

MAINTAINER Serhii Hidenko "shidenko97@gmail.com"

RUN mkdir -p /www/chat/
WORKDIR /www/chat

ADD . /www/chat

RUN pip install -r requirements.txt

CMD python main.py