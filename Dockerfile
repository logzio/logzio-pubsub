FROM python:3.7-alpine

ENV PACKAGE=filebeat-7.3.1-linux-x86_64.tar.gz

RUN mkdir -p /usr/local/etc/filebeat && \
    mkdir -p /etc/pki/tls/certs

WORKDIR /usr/local/etc/filebeat

COPY requirements.txt /usr/local/etc/filebeat/requirements.txt

RUN apk add --update --no-cache libc6-compat wget tar && \
	wget https://artifacts.elastic.co/downloads/beats/filebeat/$PACKAGE && \
    tar --strip-components=1 -zxf "$PACKAGE" && \
    rm -f "$PACKAGE" && \
    wget -P /etc/pki/tls/certs/ https://raw.githubusercontent.com/logzio/public-certificates/master/COMODORSADomainValidationSecureServerCA.crt && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY filebeat.yml /usr/local/etc/filebeat/filebeat.yml
#COPY data.yml /usr/local/etc/filebeat/data.yml
#COPY credential-file.json /usr/local/etc/filebeat/credential-file.json
COPY filebeat-yml-script.py /usr/local/etc/filebeat/filebeat-yml-script.py
#RUN cat /usr/local/etc/filebeat/filebeat.yml

CMD ["python","filebeat-yml-script.py"]