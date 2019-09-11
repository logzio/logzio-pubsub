# logzio-pubsub

logzio-pubsub is a Docker container that uses Filebeat to collect logs from Google Pub/Sub and forward those logs to your Logz.io account.

To use this container, you'll need to build a Publishers/Subscribers data file (Step 1) and export your logs by creating sinks (Step 2).
logzio-pubsub uses this data to generate a valid Filebeat configuration for the container.
//?logzio-pubsub mounts docker.sock and the Docker logs directory to the container itself, allowing Filebeat to collect the logs and metadata.

//?logzio-pubsub ships logs only.

##logzio-pubsub setup

### 1. Build your YAML data file called "data.yml"
```yml
logzio-pubsub:
    token: <LOGZIO_ACCOUNT_TOKEN>
    publishers:
    #for every publisher : fill in project id, topic id, publisher and subscribers details, as given from pubsub:
    <
    #for publisher 1:
    - project_id: <project id>
      credentials_file: <{$PATH}/credential-file.json>
      topic_id: <topic id>
      subscriptions: <firstSubName, seconedSubName, thirdSubName, ...>
      type: <name your log type as a key>

    #for publisher 2:
     - project_id: <project id>
      credentials_file: <{$PATH}/credential-file.json>
      topic_id: <topic id>
      subscriptions: <firstSubName, seconedSubName, thirdSubName, ...>
      type: <name your log type as a key>

    #and so on...
    >
```
Get your Logz.io [token](https://app.logz.io/#/dashboard/settings/general).
View example in [data-example.yml](https://github.com/logzio/logzio-pubsub/blob/develop/data-example.yml).

### 2. Create an export Sink
Create a sink for exporting your logs [here](https://cloud.google.com/logging/docs/export/configure_export_v2).

### 3. Pull the Docker image

Download the logzio/logzio-pubsub image:

```shell
docker pull logzio/logzio-pubsub
```

### 4. Run the container

For a complete list of options, see the parameters below the code block.👇

```shell
docker run --name logzio-pubsub \
-v /Users/ronishaham/Desktop/Roni/APP/data.yml:/usr/local/etc/filebeat/data.yml
-v /Users/ronishaham/Desktop/Roni/APP/credential-file.json:/usr/local/etc/filebeat/credential-file.json
logzio/logzio-pubsub
```

### 5. Check Logz.io for your logs

Spin up your Docker containers if you haven’t done so already. Give your logs a few minutes to get from your system to ours, and then open [Kibana](https://app.logz.io/#/dashboard/kibana).