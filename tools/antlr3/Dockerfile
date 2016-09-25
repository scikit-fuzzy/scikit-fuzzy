FROM openjdk:7

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

RUN apt-get update -qq && apt-get install -y locales -qq && locale-gen en_US.UTF-8
RUN dpkg-reconfigure --frontend noninteractive locales
ENV LANG=en_US.UTF-8

WORKDIR /usr/local/lib
RUN wget http://www.antlr3.org/download/antlr-3.1.3.jar

VOLUME /data
WORKDIR /data