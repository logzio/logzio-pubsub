# Pub/Sub to Logz.io

## Setup

Google Cloud Platform (GCP) Stackdriver collects logs and metrics from your cloud services.
You can use Google Cloud Pub/Sub to forward your logs from Stackdriver to Logz.io.

### Configuration

**You'll need**:
[Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts),
[a GCP project](https://console.cloud.google.com/projectcreate),
[a GCP Pub/Sub topic and subscribers](https://cloud.google.com/pubsub/docs/quickstart-console) to your GCP project

#### 1.  Export your logs to Pub/Sub

Set up a sink to export your logs to Pub/Sub.

For more information, see [Exporting with the Logs Viewer](https://cloud.google.com/logging/docs/export/configure_export_v2) from Google Cloud.

#### 2.  Build your credentials file

Make a folder for the files you'll be working with.

```shell
mkdir logzio-pubsub && cd logzio-pubsub
```

Build your credentials file using your Google Cloud project ID.

```shell
wget https://raw.githubusercontent.com/logzio/logzio-pubsub/master/Makefile \
&& make PROJECT_ID=<project_id>
```

Run this command for each project you're working with.

#### 3.  Build your Pub/Sub input YAML file

Make `pubsub-input.yml`, which will hold your Pub/Sub input configuration.

```shell
touch pubsub-input.yml
```

Open `pubsub-input.yml` in your text editor, and paste this code block.

Complete configuration instructions are below the code block. 👇

```yaml
logzio-pubsub:
listener: <<LISTENER-HOST>>

pubsubs:
- project_id: PROJECT-1_ID
credentials_file: ./credentials-file.json
token: <<SHIPPING-TOKEN>>
topic_id: TOPIC-1_ID
subscriptions: ["SUB1_ID", "SUB2_ID", "SUB3_ID"]
type: stackdriver

- project_id: PROJECT-1_ID
credentials_file: ./credentials-file.json
token: <<SHIPPING-TOKEN>>
topic_id: TOPIC-2_ID
subscriptions: ["SUB1_ID", "SUB2_ID", "SUB3_ID"]
type: stackdriver

- project_id: PROJECT-3_ID
credentials_file: ./credentials-file.json
token: <<SHIPPING-TOKEN>>
topic_id: TOPIC-1_ID
subscriptions: ["SUB1_ID", "SUB2_ID", "SUB3_ID"]
type: stackdriver
```

**Configuration instructions**

**Note**:
For extra guidance,
please see the [sample configuration YAML](https://github.com/logzio/logzio-pubsub/blob/master/pubsub-input-example.yml).

| Parameter | Description |
|---|---|
| listener | The Logz.io listener host. <br> Replace `<<LISTENER-HOST>>` with your region's listener host (for example, `listener.logz.io`). For more information on finding your account's region, see [Account region](https://docs.logz.io/user-guide/accounts/account-region.html). |
| pubsubs | This is an array of one or more GCP subscriptions.For each subscription, provide topic and subscriptions IDs, as given from Pub/Sub. |
| token | Your Logz.io shipping token. Include this with each project under `pubsubs`. <br> Replace `<<SHIPPING-TOKEN>>` with the [token](https://app.logz.io/#/dashboard/settings/general) of the account you want to ship to. |

#### 4.  Pull the Docker image

Download the logzio/logzio-pubsub image:

```shell
docker pull logzio/logzio-pubsub
```

#### 5.  Run the container

Run this command from `logzio-pubsub/`,
where you stored `pubsub-input.yml`
and `credentials-file.json`.

```shell
docker run --name logzio-pubsub \
-v ./pubsub-input.yml:/logzio-pubsub/pubsub-input.yml \
-v ./credentials-file.json:/logzio-pubsub/credentials-file.json \
logzio/logzio-pubsub
```

#### 6.  Check Logz.io for your logs

Spin up your Docker containers if you haven’t done so already.

Give your logs some time to get from your system to ours,
and then open [Kibana](https://app.logz.io/#/dashboard/kibana).
