FROM python:3.10.14

WORKDIR /workdir

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app app
COPY core core
COPY main.py main.py


