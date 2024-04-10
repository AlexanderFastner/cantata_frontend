FROM continuumio/miniconda3
 
RUN mkdir wd
WORKDIR wd

ENV DASH_DEBUG_MODE True
COPY app/requirements.txt .
RUN conda install -c conda-forge --file requirements.txt --yes

#TODO replace this with get from git repo
COPY app/ ./app
COPY data/ ./data
#TODO replace with wget to aln data
#COPY ../cantata_data/gb/ ./gb


EXPOSE 8050
CMD ["python3", "app/app.py"]