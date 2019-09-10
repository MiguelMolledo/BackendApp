FROM python:3.7-alpine

MAINTAINER Miguel Molledo

#RUN apk --no-cache add ca-certificates=20190108-r0 libc6-compat=1.1.19-r10

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add  --update --no-cache postgresql-client
run apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

