# logzio-pubsub

logzio-pubsub is a Docker container that uses Filebeat to collect logs from Google Cloud Platform through Pub/Sub and forward those logs to your Logz.io account.
<br/>

To use this container, you'll need:
1. Google Cloud SDK installed.
2. A Google Cloud Platform project.
3. Topics and subscribers to your project, created on Cloud Pub/Sub.
4. A Sink to export your logs, created on Stackdriver.
5. A Pub/Sub input YAML file.

To complete these stages please follow the pre-setup. // link to pre-setup section <br/>
If you already have those go to logzio-pubsub setup. // link to setup section

## Pre-setup

### Quickstart with Cloud Pub/Sub
  Make sure you have Google Cloud SDK.
  If you don't, [follow these steps](https://cloud.google.com/sdk/docs/downloads-versioned-archives).

  If gcloud isn't recognized run:
  ```source '[path-to-my-home]/google-cloud-sdk/path.bash.inc'```

  Read about [Cloud Pub/Sub](https://cloud.google.com/pubsub/docs/overview).<br/>
  To create Cloud Pub/Sub topics and subscribers to your GCP project, [follow these steps](https://cloud.google.com/pubsub/docs/quickstart-console).<br/>
    
### Export your logs
 To create a sink to export your logs, [follow these steps](https://cloud.google.com/logging/docs/export/configure_export_v2).<br/> Use Cloud Pub/Sub as the destination.
 
### Build your credentials file
Download the file [Makefile](https://github.com/logzio/logzio-pubsub/blob/develop/Makefile) and run:<br/>
 ```make PROJECT_ID=<project_id>```<br/>
Credentials-file.json has been created in your local path.<br/>
To support multiple projects repeat with every project id.
 
### Build your Pub/Sub input YAML file
Build a YAML file called "pubsub-input.yml".<br/>
Fill it in the format as follows:<br/>
For every topic fill in project, topic and subscriptions IDs, as given from Pub/Sub.<br/>
Get your Logz.io [token](https://app.logz.io/#/dashboard/settings/general).<br/>
Get your Logz.io [listener url](https://docs.logz.io/user-guide/accounts/account-region.html), according to your region.<br/>
View example in [pubsub-input-example.yml](https://github.com/logzio/logzio-pubsub/blob/develop/pubsub-input-example.yml).

```yml
logzio-pubsub:
    listener: <"LISTENER_URL">
    pubsubs:
    - project_id: <PROJECT-1_ID>
      credentials_file: /logzio-pubsub/credentials-file.json 
      token: <LOGZIO_ACCOUNT_TOKEN>
      topic_id: <TOPIC-1_ID>
      subscriptions: <SUB1_ID, SUB2_ID, SUB3_ID, ...>
      type: <name your log type as a key>

    - project_id: <PROJECT-1_ID>
      credentials_file: /logzio-pubsub/credentials-file.json
      token: <LOGZIO_ACCOUNT_TOKEN>
      topic_id: <TOPIC-2_ID>
      subscriptions: <SUB1_ID, SUB2_ID, SUB3_ID, ...>
      type: <name your log type as a key>

    - project_id: <PROJECT-2_ID>
      credentials_file: /logzio-pubsub/credentials-file-2.json 
      token: <LOGZIO_ACCOUNT_TOKEN>
      topic_id: <TOPIC-1_ID>
      subscriptions: <SUB1_ID, SUB2_ID, SUB3_ID, ...>
      type: <name your log type as a key>

    #and so on...
    
```
## logzio-pubsub setup

### 1. Pull the Docker image

Download the logzio/logzio-pubsub image:

```shell
docker pull logzio/logzio-pubsub
```

### 2. Run the container

```shell
docker run --name logzio-pubsub \
-v PATH/TO/YOUR/FILE/pubsub-input.yml:/logzio-pubsub/pubsub-input.yml \
-v PATH/TO/YOUR/FILE/credentials-file.json:/logzio-pubsub/credentials-file.json \
logzio/logzio-pubsub
```

### 3. Check Logz.io for your logs

Spin up your Docker containers if you haven’t done so already. Give your logs a few minutes to get from your system to ours, and then open [Kibana](https://app.logz.io/#/dashboard/kibana).
