FROM python:3.8-slim-buster
RUN apt-get update
RUN apt-get install nano
 
RUN mkdir wd
WORKDIR wd

ENV DASH_DEBUG_MODE True
COPY app/requirements.txt .
#RUN pip3 install -r requirements.txt
RUN conda install -r requirements.txt

COPY app/ ./

EXPOSE 8050
CMD ["gunicorn", "--bind", "0.0.0.0:8050", "app:server"]