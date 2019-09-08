FROM python:3.7-alpine

MAINTAINER Miguel Molledo

#RUN apk --no-cache add ca-certificates=20190108-r0 libc6-compat=1.1.19-r10

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user

