"""File server API using Flask micro services"""

# pynix-file-server
#
# Copyright (c) 2017 Lahiru Pathirage
#
# pynix-file-server is a free application.you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
# pynix-file-server is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details. See COPYING for a copy of the GNU General
# Public License. If not, see http://www.gnu.org/licenses/.

# Import third party modules
from flask import Flask

# Import application level modules
from controller import api_handler
from utility import YamlReader


# Read YAML and set configurations variables
settings_data = YamlReader("config.yml").get_data()


def run_flask_app():
    file_server = Flask(__name__)

    # Set blueprints from controller package
    file_server.register_blueprint(api_handler)

    # Run flask server
    file_server.run(
        host=settings_data["hostname"],
        port=settings_data["port"],
        threaded=True,
        debug=True
    )


def main():
    run_flask_app()


if __name__ == '__main__':
    main()
