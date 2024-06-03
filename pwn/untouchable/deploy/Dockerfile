FROM ubuntu:22.04

RUN apt-get -y update
RUN apt-get -y install socat

RUN useradd -m ctf
RUN mkdir /app
WORKDIR /app

COPY flag /app
COPY untouchable /app

USER ctf

EXPOSE 17171
CMD socat tcp-listen:17171,reuseaddr,fork exec:"./untouchable"
