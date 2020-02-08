import requests
from flask import Flask, jsonify
from core.utils import read_config


class DemoServer:
    def __init__(self, config_path="config.yml"):
        self.config = read_config(config_path)
        self.classifier_url = None
        self.app = None

    def create(self):
        # create Flask app
        server_cfg = self.config["server"]
        name = server_cfg["name"]
        template_dir = server_cfg["template_dir"]
        static_dir = server_cfg["static_dir"]

        self.app = Flask(name, template_folder=template_dir, static_folder=static_dir)

        # create classifier url
        classifier_cfg = self.config["classifier"]
        classifier_host = classifier_cfg["host"]
        classifier_port = classifier_cfg["port"]
        classifier_endpoint = classifier_cfg["endpoint"]

        self.classifier_url = f"http://{classifier_host}:{classifier_port}/{classifier_endpoint}"

        return self.app

    def run(self):
        if self.app is None:
            raise Exception("ERROR: create server first")

        server_cfg = self.config["server"]
        host = server_cfg["host"]
        port = server_cfg["port"]
        debug = server_cfg["debug"]

        self.app.run(host=host, port=port, debug=debug)

    def classify(self, image):
        # put to store + log(ts, userid, image.size, project, uid, path)
        # classify + log(ts[=store.ts], project, uid, model_name, model_version, label)

        response = requests.post(self.classifier_url, files=[('img', image)])
        result = response.json()['result']

        return result
