FROM python:3.7-alpine

ENV PACKAGE=filebeat-7.3.1-linux-x86_64.tar.gz

RUN mkdir -p /var/lib/filebeat && \
    mkdir -p /etc/pki/tls/certs

WORKDIR /var/lib/filebeat

COPY requirements.txt /var/lib/filebeat/requirements.txt

RUN apk add --update --no-cache libc6-compat wget tar && \
    apk add --update make && \
    wget https://artifacts.elastic.co/downloads/beats/filebeat/$PACKAGE && \
    tar --strip-components=1 -zxf "$PACKAGE" && \
    rm -f "$PACKAGE" && \
    wget -P /etc/pki/tls/certs/ https://raw.githubusercontent.com/logzio/public-certificates/master/COMODORSADomainValidationSecureServerCA.crt && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY filebeat.yml /var/lib/filebeat/filebeat.yml
COPY filebeat-yml-script.py /var/lib/filebeat/filebeat-yml-script.py

RUN chown -R root /var/lib/filebeat/
CMD ["python","filebeat-yml-script.py"]


