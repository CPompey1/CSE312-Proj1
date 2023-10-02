FROM python:3.8

ENV  HOME /root

WORKDIR /root
ENV FLASK_APP server.py
ENV FLASK_ENV development

RUN apt update
RUN apt upgrade
RUN pip install Flask
COPY . .
CMD  python3 -u server.py