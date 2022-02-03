FROM python:3.8

WORKDIR /code

RUN pip install -U pip wheel

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .
