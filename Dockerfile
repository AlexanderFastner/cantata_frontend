FROM continuumio/miniconda3
 
RUN mkdir wd
WORKDIR /wd

ENV DASH_DEBUG_MODE True
COPY app/requirements.txt .

RUN conda install -c conda-forge --file requirements.txt --yes

COPY app/ ./app
COPY data/ ./data
COPY gb/ ./gb

WORKDIR /wd/app/
EXPOSE 8050

CMD gunicorn --workers=1 --threads=1 -b 0.0.0.0:$PORT app:server
#----------------------------------------------------------------
#make reqs file
#conda list -e > requirements.txt
#----------------------------------------------------------------
#USAGE
#----------------------------------------------------------------
#for heroku
#heroku container:login
#heroku container:push web
#heroku container:release web
#----------------------------------------------------------------
#for local docker test
#docker build -t cantata .
#docker run -p 8050:8050 -e PORT=8050 cantata
#----------------------------------------------------------------