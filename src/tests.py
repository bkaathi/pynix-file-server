"""Unit tests"""

# Tests for Flask blue print.
# Copyright (c) 2017 Lahiru Pathirage <http://lahiru.site>

# Python system level packages
import os
import requests
import unittest

# Third party packages
from flask import Flask
from flask_testing import LiveServerTestCase

# Application level modules
from controller import api_handler
from utility import YamlReader


# Read settings from config file
settings_data = YamlReader("config.yml").get_data()

# Create file resources directory if there is not.
if not os.path.exists(settings_data["file_directory"]):
    os.makedirs(settings_data["file_directory"])


class UnitTest(LiveServerTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.register_blueprint(api_handler)

        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = settings_data["port"]
        app.config['LIVESERVER_TIMEOUT'] = 10

        return app

    def step_delete_file(self):

        response = requests.delete(
            self.get_server_url() + "/files/config.yml",
            auth=(
                settings_data["username"],
                settings_data["password"]
            )
        )

        self.assertEqual(response.status_code, 200)

        response = requests.delete(
            self.get_server_url() + "/files/temp.yml",
            auth=(
                settings_data["username"],
                settings_data["password"]
            )
        )

        self.assertEqual(response.status_code, 200)

    def step_download_file(self):
        response = requests.get(
            self.get_server_url() + "/files/config.yml",
            auth=(
                settings_data["username"],
                settings_data["password"]
            ),
            stream=True
        )

        if response.status_code == 200:
            with open(
                settings_data["file_directory"] + "/temp.yml",
                "wb+"
            ) as file_stream:
                for chunk in file_stream:
                    file_stream.write(chunk)

        self.assertEqual(response.status_code, 200)

    def step_get_files_list(self):
        response = requests.get(
            self.get_server_url() + "/files",
            auth=(
                settings_data["username"],
                settings_data["password"]
            )
        )

        self.assertNotIsInstance(response.json, str)

    def step_upload_file(self):
        file_resource = open("config.yml", "rb")

        response = requests.post(
            self.get_server_url() + "/files",
            auth=(
                settings_data["username"],
                settings_data["password"]
            ),
            files={"file": file_resource}
        )

        # Close file to avoid memory leaks
        file_resource.close()

        self.assertEqual(response.status_code, 200)

    def test_server_up_and_running(self):
        response = requests.get(
            self.get_server_url(),
            auth=(
                settings_data["username"],
                settings_data["password"]
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_steps(self):
        """Test case order"""
        self.step_upload_file()
        self.step_download_file()
        self.step_get_files_list()
        self.step_delete_file()

        # Close settings file


if __name__ == '__main__':
    unittest.main()
