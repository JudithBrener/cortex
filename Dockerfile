FROM python:3.8-slim-buster

EXPOSE 8000
COPY requirements.txt /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Add docker-compose-wait script
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

COPY cortex /cortex