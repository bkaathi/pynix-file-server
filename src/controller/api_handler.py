"""Handle and route HTTP API"""

# Blueprint to handle HTTP requests.
#
# Uses HTTP basic authentication to secure and provides HTTP APIs to
# check server status, get list of files, get file by file name, delete file by
# file name, upload files.
#
# HTTP API::
#
#   /                   GET     check server status
#   /files              GET     get list of files
#   /files/:file_name   GET     get file by file name
#   /files/:file_name   DELETE  delete file by file name
#   /files              POST    upload file
#
# Copyright (c) 2017 Lahiru Pathirage <http://lahiru.site>


# Python system packages
import os

# Third party packages
from functools import wraps
from flask import Blueprint, jsonify, Response, request, send_from_directory
from werkzeug.utils import secure_filename

# Application level modules
from utility import YamlReader


# Read settings from config file
settings_data = YamlReader("config.yml").get_data()

# Initiate Flask blueprint
api_handler = Blueprint("api_handler", __name__)


def check_auth(username, password):
    """Check authentication data"""
    return (
        username == settings_data["username"]
        and password == str(settings_data["password"])
    )


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        "Authentication failure\n",
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    """Handle authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()

        return f(*args, **kwargs)

    return decorated


@api_handler.route("/")
@requires_auth
def get_server_status():
    """Returns a string if server is up and running"""
    return Response(
        "Server is functional\n",
        200,
        {'ContentType': 'application/json'}
    )


@api_handler.route("/files")
@requires_auth
def get_files_list():
    """Returns a list of files in the server"""
    try:
        return jsonify(
            os.listdir(settings_data["file_directory"]),
        )

    except:
        return Response(
            "Internal server error\n",
            500,
            {'ContentType': 'application/json'}
        )


@api_handler.route("/files/<name>", methods=["GET"])
@requires_auth
def get_file_by_file_name(name):
    """Check for file in resources directory and return if"""
    if name in os.listdir(settings_data["file_directory"]):
        return send_from_directory(
            directory=os.path.abspath(settings_data["file_directory"]),
            filename=name,
        )

    else:
        return Response(
            name + " not found in the server\n",
            400,
            {'ContentType': 'application/json'}
        )


@api_handler.route("/files/<name>", methods=["DELETE"])
@requires_auth
def remove_file_by_file_name(name):
    """Find file in resources directory and delete if"""
    if name in os.listdir(settings_data["file_directory"]):
        os.remove(
            settings_data["file_directory"] + "/" + name
        )

        return Response(
            name + " deleted successfully\n",
            200,
            {'ContentType': 'application/json'}
        )

    else:
        return Response(
            name + " not found in the server\n",
            400,
            {'ContentType': 'application/json'}
        )


@api_handler.route("/files", methods=["POST"])
@requires_auth
def save_new_file():
    """Handle file uploading, save files in resources directory"""
    file = request.files["file"]

    if file:
        file_name = secure_filename(file.filename)
        file.save(
            os.path.join(settings_data["file_directory"], file_name)
        )

        return Response(
            file_name + " uploaded successfully\n",
            200,
            {'ContentType': 'application/json'}
        )

    else:
        return Response(
            "Invalid file type\n",
            400,
            {'ContentType': 'application/json'}
        )
