FROM python:3.7-slim

ENV PACKAGE=filebeat-7.3.1-linux-x86_64.tar.gz
WORKDIR /logzio-pubsub

RUN mkdir -p /logzio-pubsub && \
    mkdir -p /etc/pki/tls/certs

COPY requirements.txt /logzio-pubsub/requirements.txt
COPY filebeat.yml /logzio-pubsub/filebeat.yml
COPY filebeat-yml-script.py  /logzio-pubsub/filebeat-yml-script.py

RUN apt-get update && \
    apt-get install -y \
    curl \
    wget && \
    curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.3.2-amd64.deb && \
    dpkg -i filebeat-7.3.2-amd64.deb && \
    wget -P /etc/pki/tls/certs/ https://raw.githubusercontent.com/logzio/public-certificates/master/TrustExternalCARoot_and_USERTrustRSAAAACA.crt && \
    pip install -r requirements.txt && \
    rm requirements.txt


CMD ["python","filebeat-yml-script.py"]


