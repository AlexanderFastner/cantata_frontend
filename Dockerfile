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
#TODO fix this wgsi nonsense
CMD [ "gunicorn", "--workers=1", "--threads=2", "-b 0.0.0.0:8050", "app:server"]
#docker build -t cantata-heroku .
#docker run -p 8050:8050 -e PORT=8050 cantata-heroku