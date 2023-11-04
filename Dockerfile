FROM python:3.8-alpine
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/scripts:${PATH}"

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN apk add --update --no-cache mysql-client mysql-dev jpeg-dev mariadb-dev gcc
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers musl-dev zlib zlib-dev 
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN cp /usr/share/zoneinfo/America/Bogota /etc/localtime

RUN mkdir /code
WORKDIR /code
COPY . /code/