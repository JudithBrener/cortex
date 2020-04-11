FROM python:3.8-slim-buster

COPY . /cortex-app
WORKDIR /cortex-app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python -m cortex.server run-server \
      -h '0.0.0.0'          \
      -p 8000                 \
      'rabbitmq://127.0.0.1:5672/'