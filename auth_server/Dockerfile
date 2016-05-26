FROM debian:jessie
MAINTAINER Roman Suvorov windj007@gmail.com

RUN apt-get clean && apt-get update && apt-get install -yqq \
    python python-pip python-dev build-essential \
    tar bzip2 apache2 libapache2-mod-wsgi sed python-mysqldb \
    libffi-dev libssl-dev
RUN pip install --upgrade cffi django==1.8.2 PyJWT django-urlcrypt \
    cryptography==1.1.1 pycrypto pytz

RUN rm /etc/apache2/sites-enabled/*
ADD auth_server.conf /etc/apache2/sites-enabled/auth_server.conf
ADD ssl.conf /etc/apache2/conf-enabled/ssl.conf
ADD ports.conf /etc/apache2/ports.conf
RUN mkdir -p /var/cache/httpd/mod_ssl/ssl_scache
RUN a2enmod ssl rewrite
RUN ln -sf /dev/stderr /var/log/apache2/error.log


ADD auth_server/ /srv/auth_server/

VOLUME /var/log/apache2

EXPOSE 80 443

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
