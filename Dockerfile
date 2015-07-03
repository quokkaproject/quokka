FROM ubuntu:14.04

MAINTAINER Bruno Rocha <rochacbruno@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install nginx sed python-pip python-dev uwsgi-plugin-python supervisor libjpeg-dev

RUN mkdir -p /var/log/nginx/app
RUN mkdir -p /var/log/uwsgi/app/


RUN rm /etc/nginx/sites-enabled/default
COPY quokka_nginx.conf /etc/nginx/sites-available/quokka.conf
RUN ln -s /etc/nginx/sites-available/quokka.conf /etc/nginx/sites-enabled/quokka.conf
COPY uwsgi.ini /var/www/app/

RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

copy . /quokka
RUN pip install -r requirements.txt

CMD ["/usr/bin/supervisord"]
