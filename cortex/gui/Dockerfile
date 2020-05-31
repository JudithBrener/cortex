FROM nikolaik/python-nodejs:python3.8-nodejs14
WORKDIR /cortex/gui
COPY ./cortex/gui/gui_vue/package*.json ./gui_vue/
WORKDIR /cortex/gui/gui_vue
RUN npm install
WORKDIR /cortex/gui
COPY ./cortex/gui/ .
WORKDIR /cortex/gui/gui_vue
RUN npm run build

#FROM python:3.8-slim-buster as production-stage
WORKDIR /cortex/gui
EXPOSE 8080
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Add docker-compose-wait script
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait
WORKDIR /