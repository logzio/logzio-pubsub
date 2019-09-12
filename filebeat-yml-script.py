import os
from ruamel.yaml import YAML
import json

# set vars and consts

FILEBEAT_CONF_PATH = "/usr/local/etc/filebeat/filebeat.yml"

def _add_topic():
    yaml = YAML()
    with open("./filebeat.yml", "r") as filebeat_yml:
        config_dict = yaml.load(filebeat_yml)

    with open("./pubsub-data.yml", "r") as data_yml:
        pubsub_data_dictionary = yaml.load(data_yml)

    amount_of_publishers = range(len(pubsub_data_dictionary["logzio-pubsub"]))
    for publisher_index in amount_of_publishers:
        amount_of_subscribers = range(len(pubsub_data_dictionary["logzio-pubsub"]["publishers"][publisher_index]["subscriptions"]))
        for subscriber_index in amount_of_subscribers:
            subscriber_dict = {
                "type": "google-pubsub",
                "project_id": pubsub_data_dictionary["logzio-pubsub"]["publishers"][publisher_index]["project_id"],
                "topic": pubsub_data_dictionary["logzio-pubsub"]["publishers"][publisher_index]["topic_id"],
                "credentials_file": pubsub_data_dictionary["logzio-pubsub"]["publishers"][publisher_index][
                    "credentials_file"],
                "subscription.name":
                    pubsub_data_dictionary["logzio-pubsub"]["publishers"][publisher_index]["subscriptions"][
                        subscriber_index],
                "fields":
                    {
                        "logzio_codec": "JSON",
                        "token": pubsub_data_dictionary["logzio-pubsub"]["token"],
                        "type": pubsub_data_dictionary["logzio-pubsub"]["publishers"][publisher_index]["type"],
                    },
                "fields_under_root": "true",
                "encoding": "utf-8"
            }
            config_dict["filebeat.inputs"].append(subscriber_dict)

    config_dict["output"]["logstash"]["hosts"].append("listener.logz.io:5015")

    with open(FILEBEAT_CONF_PATH, "w+") as filebeat_yml:
        yaml.dump(config_dict, filebeat_yml)

_add_topic()

os.system("./filebeat -e")
