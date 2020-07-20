# Pub/Sub to Logz.io

Google Cloud Platform (GCP) Stackdriver collects logs and metrics from your cloud services.
You can use Google Cloud Pub/Sub to forward your logs from Stackdriver to Logz.io.

#### Configuration

**Before you begin, you'll need**: 
* [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)
* [a GCP project](https://console.cloud.google.com/projectcreate)
* a GCP Pub/Sub [topic and subscribers](https://cloud.google.com/pubsub/docs/quickstart-console) to your GCP project

<div class="tasklist">

##### 1. Export your logs to Stackdriver

Set up a sink to export your logs to Stackdriver.

For more information, see
[Exporting with the Logs Viewer](https://cloud.google.com/logging/docs/export/configure_export_v2)
from Google Cloud.

##### 2. Build your credentials file

Create a working directory for this step and `cd` into it, run as root.

```shell
mkdir ~/logzio-pubsub && cd ~/logzio-pubsub
```

You'll need to build a credentials file so Pub/Sub can authenticate
and get the right permissions.

You can build it through:
* [The command line](#credentials-cmd) 
* [The Cloud console](#credentials-console)

<div id ="credentials-cmd">

###### Option 1: In the command line

Build your credentials file using your Google Cloud project ID.  
Before you begin make sure your 'gcloud' cli is installed. If not, execute the following:
  1. Download the 'google-cloud-sdk' to '~/logzio-pubsub'
  2. Run  ```~/logzio-pubsub/google-cloud-sdk/install.sh```
 
Then replace '<project_id>' with your project id and run:

```shell
wget https://raw.githubusercontent.com/logzio/logzio-pubsub/master/create_credentials.py \
&& python create_credentials.py PROJECT_ID=<project_id>
```

Run this command for each project you're working with.  
**Important note: If you are renaming the file please follow [these steps](#cred-info) as well.


</div>
<div id ="credentials-console">

###### Option 2: In the Cloud Console

* Go to your project's page in [GCP Console](https://console.cloud.google.com).
In the left menu, select **IAM & admin > Service accounts**.

* At the top of the _Service accounts_ page, click **+ CREATE SERVICE ACCOUNT**.

* Give a descriptive **Service account name**, such as "logzio-credentials-file".
Click **CREATE** to continue to the _IAM/permissions_ page.

* Add the role: 'Pub/Sub Editor'.

* Click **CONTINUE** to _Grant users access to this service account_.
Click **ADD KEY + CREATE NEW KEY** to open the _Create key_ panel.
Select **JSON** and click **CREATE** to save the private key to your machine.

* Click **DONE** to return to the _Service accounts_ page.

* Rename it in the following format: '<<project-id>>-credentials.json' - replace to your project id.  
Move it to the `~/logzio-pubsub` folder you've created
at the beginning of this step.  
**Important note: If you are naming it differently please follow [these steps](#cred-info) as well.

</div>

##### 3. Build your Pub/Sub input YAML file

Make `pubsub-input.yml`, which will hold your Pub/Sub input configuration.

```shell
touch ~/logzio-pubsub/pubsub-input.yml && open ~/logzio-pubsub/pubsub-input.yml
```
Paste this code block to your opened file and complete the configuration instructions. 👇

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
** Note that YAML files are sensitive to spaces and tabs. We recommend using a YAML validator to make sure that the file structure is correct.

Click here for more information about [filebeat for Google Cloud Pub/Sub](https://www.elastic.co/guide/en/beats/filebeat/master/filebeat-input-google-pubsub.html#filebeat-input-google-pubsub).
###### Configuration instructions

| Parameter | Description |
|---|---|
| listener | The Logz.io listener host. (Default value: `listener.logz.io`) <br> Replace `<<LISTENER-HOST>>` with your region's listener host. For more information on finding your account's region, see [Account region](https://docs.logz.io/user-guide/accounts/account-region.html). |
| pubsubs | This is an array of one or more GCP subscriptions. For each topic, provide topic and subscriptions IDs, as given from Pub/Sub. |
| token | Your Logz.io shipping token. For each project under `pubsubs`. <br> Replace `<<SHIPPING-TOKEN>>` with the [token](https://app.logz.io/#/dashboard/settings/general) of the account you want to ship to. You can send your logs to different accounts that are in the same region, you can do that by inserting different tokens. |
| credentials_file (Not required, Default value: '<project_id>-credentials.json') | This field is only required if your credentials file is named differently than the default value. For an example of adding this field go to [input example file](https://github.com/logzio/logzio-pubsub/blob/master/pubsub-input-example.yml). |

##### 4. Pull the Docker image

Download the logzio/logzio-pubsub image:

```shell
docker pull logzio/logzio-pubsub
```

##### 5. Run the container

Replace <<PROJECT_ID>>  with your project id and run this command.  
Important notes:  
** If you've named your credentials file manually follow [these steps](#cred-info) as well.   
** When working with multiple topics, for every credentials file you've created add this line:  
```-v ~/logzio-pubsub/<<PROJECT_ID>>-credentials.json:/logzio-pubsub/<<PROJECT_ID>>-credentials-file.json \```
and insert your project id instead of the parameters.

```shell
docker run --name logzio-pubsub \
-v ~/logzio-pubsub/pubsub-input.yml:/logzio-pubsub/pubsub-input.yml \
-v ~/logzio-pubsub/<<PROJECT_ID>>-credentials.json:/logzio-pubsub/<<PROJECT_ID>>-credentials.json \
logzio/logzio-pubsub
```

#### 6. Check Logz.io for your logs

Spin up your Docker containers if you haven’t done so already.  
Give your logs some time to get from your system to ours,
and then open [Kibana](https://app.logz.io/#/dashboard/kibana).

<div id="cred-info">

####  Information about the credentials file
When creating the credentials file through the [command line](#credentials-cmd) your credentials file is named by default in the following format:  
'<<project_id>>-credentials.json'.  
When creating the credentials file through the [gcp console](#credentials-console) you are requested to name the file in that format.  
In both cases, if you wish to name it differently please follow these instructions:
1. On step 3 - building your 'pubsub-input.yml' file, please add the field 'credentials_file' with your credentials file's name as the value.
For an example of adding this field go to [input example file](https://github.com/logzio/logzio-pubsub/blob/master/pubsub-input-example.yml).
2. On step 5 - running the docker, for every credentials file you've created add this line:
'-v ~/logzio-pubsub/<credentials-file-name>.json:/logzio-pubsub/<credentials-file-name>.json \'
and replace '<credentials-file-name>' with your credentials file's name.
</div>

## Change log
0.0.7:
   - Updated creating credentials script and automated naming of credentials files for 'pubsub-input.yml' file.

0.0.6:
   - Fixed multiple listeners option.

0.0.5:
   - Updated a new public SSL certificate.


</div>
