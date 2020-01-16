FROM alpine:latest

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV PYTHONUNBUFFERED 1

RUN apk --update --no-cache add \
    python3 \
    python3-dev \
    postgresql-client \
    postgresql-dev
RUN apk add --no-cache \
    ca-certificates \
    && update-ca-certificates

WORKDIR /www
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY . ./
