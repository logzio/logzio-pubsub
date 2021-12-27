# Pub/Sub to Logz.io

Google Cloud Platform (GCP) Stackdriver collects logs from your cloud services.
You can use Google Cloud Pub/Sub to forward your logs from Stackdriver to Logz.io.

#### Configuration

**Before you begin, you'll need**:

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)
- [a GCP project](https://console.cloud.google.com/projectcreate)
- a GCP Pub/Sub [topic and subscribers](https://cloud.google.com/pubsub/docs/quickstart-console) to your GCP project

<div class="tasklist">

##### 1. Export your logs to Stackdriver

Set up a sink to export your logs to Stackdriver.

For more information, see
[Exporting with the Logs Viewer](https://cloud.google.com/logging/docs/export/configure_export_v2)
from Google Cloud.

##### 2. Build your credentials file

Create a working directory for this step and `cd` into it.
You'll need to run this command as root:

```shell
mkdir /etc/logzio-pubsub && cd /etc/logzio-pubsub
```

Next, you'll need to build a credentials file so Pub/Sub can authenticate
and get the right permissions.

You can build it through:

- [The command line](#credentials-cmd)
- [The Cloud console](#credentials-console)

<div id ="credentials-cmd">

###### Option 1: Build the credentials file from the command line

In this step, you'll build your credentials file using your Google Cloud project ID.
Before you begin, you'll need the gcloud command-line tool (CLI) installed. If it isn't, follow the steps to install it:

1. [Download](https://cloud.google.com/sdk/docs/quickstarts) the 'google-cloud-sdk' to '/etc/logzio-pubsub'
2. Run `source '/etc/logzio-pubsub/google-cloud-sdk/path.bash.inc'`  
   \*\*If you are not logged in to gcloud you will be requested to login through your browser.

Run the following command for each project you're working with. Replace the placeholder with your project id before running the command:

```shell
wget https://raw.githubusercontent.com/logzio/logzio-pubsub/master/create-credentials.py \
&& python create-credentials.py <<project-id>>
```

If you rename the file, follow [these steps](#cred-info) as well.

</div>
<div id ="credentials-console">

###### Option 2: Build the credentials file in the Cloud Console

- In the [GCP Console](https://console.cloud.google.com), go to your project's page.
  In the left menu, select **IAM & admin > Service accounts**.

- At the top of the _Service accounts_ page, click **+ CREATE SERVICE ACCOUNT**.

- Give a descriptive **Service account name**, such as "logzio-credentials-file".
  Click **CREATE** to continue to the _IAM/permissions_ page.

- Add the role: 'Pub/Sub Editor'.

- Click **CONTINUE** to _Grant users access to this service account_.
  Click **ADD KEY + CREATE NEW KEY** to open the _Create key_ panel.
  Select **JSON** and click **CREATE** to save the private key to your machine.

- Click **DONE** to return to the _Service accounts_ page.

- Rename the file in the following format: '<project-id>-credentials.json' - replace the parameter to your project id.  
  Move it to the `/etc/logzio-pubsub` folder you've created at the beginning of this step.

##### Variation

- If your credentials file name isn't of the default format `<<project_id>>-credentials.json`, follow [the steps below](#cred-info) as well.

</div>

##### 3. Build your Pub/Sub input YAML file

Create a file 'pubsub-input.yml' to hold your Pub/Sub input configuration.
To create the file run the following command as root. Then open the file in your text editor:

```shell
touch /etc/logzio-pubsub/pubsub-input.yml
```

Paste this code block into your file.
Complete configuration instructions are below the code block. 👇

```yaml
listener: <<LISTENER-HOST>>
pubsubs:
  - project_id: PROJECT-1_ID
    topic_id: TOPIC-1_ID
    token: <<SHIPPING-TOKEN>>
    subscriptions: [SUB1_ID, SUB2_ID, SUB3_ID]
    type: stackdriver

  - project_id: PROJECT-1_ID
    topic_id: TOPIC-2_ID
    token: <<SHIPPING-TOKEN>>
    subscriptions: [SUB1_ID, SUB2_ID, SUB3_ID]
    type: stackdriver

  - project_id: PROJECT-3_ID
    topic_id: TOPIC-1_ID
    token: <<SHIPPING-TOKEN>>
    subscriptions: [SUB1_ID, SUB2_ID, SUB3_ID]
    type: stackdriver
```

\*\* Note that YAML files are sensitive to spaces and tabs. We recommend using a YAML validator to make sure that the file structure is correct.

Click here for more information about [filebeat for Google Cloud Pub/Sub](https://www.elastic.co/guide/en/beats/filebeat/7.12/filebeat-input-gcp-pubsub.html).

###### Configuration instructions

| Parameter                                                                       | Description                                                                                                                                                                                                                                                                                                                      |
| ------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| listener                                                                        | The Logz.io listener host. (Default value: `listener.logz.io`) <br> Replace `<<LISTENER-HOST>>` with your region's listener host. For more information on finding your account's region, see [Account region](https://docs.logz.io/user-guide/accounts/account-region.html).                                                     |
| pubsubs                                                                         | This is an array of one or more GCP subscriptions. For each topic, provide topic and subscription IDs, as given from Pub/Sub.                                                                                                                                                                                                    |
| token                                                                           | Your Logz.io shipping token. For each project under `pubsubs`. <br> Replace `<<SHIPPING-TOKEN>>` with the [token](https://app.logz.io/#/dashboard/settings/general) of the account you want to ship to. You can send your logs to different accounts that are in the same region, you can do that by inserting different tokens. |
| credentials_file (Not required, Default value: '<project_id>-credentials.json') | This field is only required if your credentials file was renamed and does not have the default name. For an example of adding this field go to [input example file](https://github.com/logzio/logzio-pubsub/blob/master/pubsub-input-example.yml).                                                                               |

##### 4. Pull the Docker image

Download the logzio/logzio-pubsub image:

```shell
docker pull logzio/logzio-pubsub
```

##### 5. Run the container

Run the following command after you replace `<<PROJECT_ID>>` with your details.

```shell
docker run --name logzio-pubsub \
-v /etc/logzio-pubsub/pubsub-input.yml:/logzio-pubsub/pubsub-input.yml \
-v /etc/logzio-pubsub/<<PROJECT_ID>>-credentials.json:/logzio-pubsub/<<PROJECT_ID>>-credentials.json \
logzio/logzio-pubsub
```

###### Variations

- If you're working with multiple topics, add this line for every credentials file you've created. Insert your project id instead of the parameters:
  ```
  -v /etc/logzio-pubsub/<<PROJECT_ID>>-credentials.json:/logzio-pubsub/<<PROJECT_ID>>-credentials-file.json \
  ```
- If your credentials file name isn't of the default format `<<project_id>>-credentials.json`, follow [the steps below](#cred-info) as well.
- If you're using a Mac, you'll need to fix issues with mounting files from root directory.
  Add the path '/etc/logzio-pubsub' to your Docker File Sharing. Click [here](https://medium.com/effy-tech/fixing-the-var-folders-error-in-docker-for-mac-v2-2-3-2a40e776132d) for a guide on how to fix this issue - you can use docker desktop or manually edit your Docker configuration file.
  For more information about mounting files from the root directory click [here](https://docs.docker.com/docker-for-mac/osxfs/#namespaces).

#### 6. Check Logz.io for your logs

Spin up your Docker containers if you haven’t done so already.  
Give your logs some time to get from your system to ours,
and then open [Kibana](https://app.logz.io/#/dashboard/kibana).

<div id="cred-info">

#### If you've renamed the credentials file

The default naming convention for the credentials file is: `<<project_id>>-credentials.json`.  
When you create the credentials file through the [command line](#credentials-cmd), it is automatically named as per the default.  
If you create the credentials file using the [GCP Console](#credentials-console), you'll have the option to select the file name. We strongly recommend that you stick to the default format: `<<project_id>>-credentials.json`.  
If you decide to give the credentials file another name, please follow these instructions:

1. On step 3 - building your 'pubsub-input.yml' file, add the field 'credentials_file' with your credentials file's name as the value.  
   Go to the github project to see an [example of an input file](https://github.com/logzio/logzio-pubsub/blob/master/pubsub-input-example.yml).
2. On step 5 - running the docker, add the following line for every credentials file you've created:  
   '-v /etc/logzio-pubsub/<<credentials-file-name>>.json:/logzio-pubsub/<<credentials-file-name>>.json \'.  
   Replace `<<credentials-file-name>>` with your credentials file's name.

</div>

## Change log

0.1.0:

- Upgraded Filebeat to version 7.12.0.
- Changed yaml handler from `ruamel.yaml` to `pyyaml`.
- Added ARM support. To Build Image to support ARM please use `docker build -f Dockerfile-arm .`

0.0.7:

- Updated creating credentials script and automated naming of credentials files for 'pubsub-input.yml' file.

0.0.6:

- Fixed multiple listeners option.

0.0.5:

- Updated a new public SSL certificate.

</div>
