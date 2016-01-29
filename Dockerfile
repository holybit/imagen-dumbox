FROM python:2.7
MAINTAINER Joseph Crotty <josephcrotty@gmail.com>

# Optimixed for volume mounting on Mac YMMV
RUN groupadd -r imagen \
    && useradd -r -m -g imagen imagen \
    && usermod -u 1000 imagen \
    && usermod -G staff imagen

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY . /usr/src/app
RUN chown -R imagen:imagen /usr/src/app

USER imagen
