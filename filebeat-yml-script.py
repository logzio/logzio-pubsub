import os
import yaml

FILEBEAT_CONF_PATH = "/etc/filebeat/filebeat.yml"
credentials_files = {}
error_msg = "Your listener is invalid."


def _add_all_topics():

    with open("filebeat.yml", "r") as filebeat_yml:
        config_dict = yaml.safe_load(filebeat_yml)

    with open("pubsub-input.yml", "r") as input_yml:
        pubsub_input = yaml.safe_load(input_yml)

    for publisher in pubsub_input["pubsubs"]:
        for subscriber in publisher["subscriptions"]:
            subscriber_dict = _add_subscriber(publisher, subscriber)
            config_dict["filebeat.inputs"].append(subscriber_dict)
    try:
        listener = pubsub_input["listener"] + ":5015"
        if listener.startswith("<<LISTENER-HOST>>"):
            raise Exception(error_msg)
    except Exception:
        raise Exception(error_msg)
    config_dict["output"]["logstash"]["hosts"].append(listener)
    print("this is our listener: " + listener)
    with open(FILEBEAT_CONF_PATH, "w+") as filebeat_yml:
        yaml.dump(config_dict, filebeat_yml)


def _add_subscriber(publisher, subscriber):
    project_id = publisher["project_id"]
    credentials_file = publisher.get(
        "credentials_file", str(project_id) + "-credentials.json")
    subscriber_dict = {
        "type": "google-pubsub",
        "project_id": project_id,
        "topic": publisher["topic_id"],
        "credentials_file": "/logzio-pubsub/" + credentials_file,
        "subscription.name": subscriber,
        "fields":
            {
                "logzio_codec": "json",
                "token": publisher["token"],
                "type": publisher.get("type", "google-pubsub"),
        },
        "fields_under_root": "true",
        "encoding": "utf-8"
    }
    return subscriber_dict


_add_all_topics()

os.system("filebeat -e")
