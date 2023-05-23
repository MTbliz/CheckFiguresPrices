FROM bitnami/spark:3.3.2
USER root
RUN apt-get update -yqq && \
    apt-get upgrade -yqq && \
    apt-get install -yqq --no-install-recommends \ 
    wget \
    && apt-get clean

WORKDIR /opt
RUN mkdir spark
RUN mkdir spark/jars

RUN wget  https://jdbc.postgresql.org/download/postgresql-42.2.5.jar
RUN mv postgresql-42.2.5.jar /opt/spark/jars/