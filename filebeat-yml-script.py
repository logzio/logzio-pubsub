import os
from ruamel.yaml import YAML

FILEBEAT_CONF_PATH = "/var/lib/filebeat/filebeat.yml"
credentials_files = {}


def _add_all_topics():
    yaml = YAML()

    with open("filebeat.yml", "r") as filebeat_yml:
        config_dict = yaml.load(filebeat_yml)

    with open("pubsub-input.yml", "r") as input_yml:
        pubsub_input = yaml.load(input_yml)

    for publisher in pubsub_input["logzio-pubsub"]["pubsubs"]:
        for subscriber in publisher["subscriptions"]:
            subscriber_dict = _add_subscriber(publisher, subscriber)
            config_dict["filebeat.inputs"].append(subscriber_dict)

    config_dict["output"]["logstash"]["hosts"].append(pubsub_input["logzio-pubsub"]["listener"])

    with open(FILEBEAT_CONF_PATH, "w+") as filebeat_yml:
        yaml.dump(config_dict, filebeat_yml)


def _add_subscriber(publisher, subscriber):
    project_id = publisher["project_id"]

    subscriber_dict = {
        "type": "google-pubsub",
        "project_id": project_id,
        "topic": publisher["topic_id"],
        "credentials_file": publisher["credentials_file"],
        "subscription.name": subscriber,
        "fields":
            {
                "logzio_codec": "JSON",
                "token": publisher["token"],
                "type": publisher["type"],
            },
        "fields_under_root": "true",
        "encoding": "utf-8"
    }
    return subscriber_dict


_add_all_topics()

os.system("./filebeat -e")
