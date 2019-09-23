FROM python:3.7-alpine

ENV PACKAGE=filebeat-7.3.1-linux-x86_64.tar.gz

RUN mkdir -p /var/lib/filebeat && \
    mkdir -p /etc/pki/tls/certs

WORKDIR /var/lib/filebeat

COPY requirements.txt /var/lib/filebeat/requirements.txt

RUN apk add --update \
    curl \
    && rm -rf /var/cache/apk/*

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
  && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
  && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin


RUN apk add --update --no-cache libc6-compat wget tar && \
    apk add --update make && \
#    gcloud auth application-default login && \
    gcloud auth login 4/rQEvZk8Uxz_KCdxwibxwmeqy4hTI-KulapQDn6fat_eoIrDQi-YIPBw && \
    gcloud init && \
    wget https://artifacts.elastic.co/downloads/beats/filebeat/$PACKAGE && \
    tar --strip-components=1 -zxf "$PACKAGE" && \
    rm -f "$PACKAGE" && \
    wget -P /etc/pki/tls/certs/ https://raw.githubusercontent.com/logzio/public-certificates/master/COMODORSADomainValidationSecureServerCA.crt && \
    pip install -r requirements.txt && \
    rm requirements.txt

COPY filebeat.yml /var/lib/filebeat/filebeat.yml
COPY filebeat-yml-script.py /var/lib/filebeat/filebeat-yml-script.py
COPY Makefile /var/lib/filebeat/Makefile

RUN chown -R root /var/lib/filebeat/
CMD ["python","filebeat-yml-script.py"]


