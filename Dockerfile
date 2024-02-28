FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install nano
 
RUN mkdir wd
WORKDIR wd

ENV DASH_DEBUG_MODE True
COPY app/requirements.txt .
RUN pip3 install -r requirements.txt
  
COPY app/ ./
