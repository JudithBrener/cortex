FROM python:3.8-slim-buster

EXPOSE 8000
COPY requirements.txt /
RUN pip install -r requirements.txt

COPY cortex /cortex