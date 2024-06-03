FROM dockerhub.timeweb.cloud/library/ubuntu:22.04

RUN apt-get -y update
RUN apt-get -y install socat gcc

RUN useradd -m ctf
RUN mkdir /app
WORKDIR /app

COPY main.c /app
COPY flag /app

RUN gcc main.c -o ROP -no-pie -fno-stack-protector
RUN rm main.c

USER ctf

EXPOSE 37373
CMD socat tcp-listen:37373,reuseaddr,fork exec:"./ROP"
