FROM python:3.8
MAINTAINER Kim Young Jin <with.alpha.and.omega@gmail.com>

ENV FLASK_APP run.py
ENV FLASK_ENV production

# for mysql running status check
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev default-mysql-server

RUN mkdir /project
ADD . /project

WORKDIR /project
RUN pip install -r requirments.txt

RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ./docker-entrypoint.sh