[![Build Status](https://travis-ci.org/lpsandaruwan/pynix-file-server.png)](https://travis-ci.org/lpsandaruwan/pynix-file-server)

# pynix-file-server
Simple Python Flask file server using Nix package manager.

### Requirements
Make sure you have installed `Nix package manager`, if not please see, [https://nixos.org/nix/download.html](https://nixos.org/nix/download.html).

### Configurations
Application runtime configuration settings are in the `config.yml` file.
Change configurations as you wish.
```bash
hostname: 0.0.0.0
port: 5000
file_directory: ./files
username: admin
password: 1234
```

### Running
Once you have installed and configured nix package manager, from the source directory run,
```bash
nix-shell --run "python src/main.py"
```

### Testing
To run unit tests, run,
```bash
nix-shell test.nix --run "python src/tests.py"
```

To test manually use `curl` or any appropriate tool.
```bash
# Server status
curl -v -u admin:1234 http://localhost:5000

# Get a list of files
curl -v -u admin:1234 http://localhost:5000/files

# Retrieve a file
curl -v -u admin:1234 http://localhost:5000/files/:filename

# Upload a file
curl -v -u admin:1234 -X POST -F "file=@PATH_TO_FILE" http://localhost:5000/files

# Delete a file
curl -v -u admin:1234 -X DELETE http://localhost:5000/files/:fillename
```


### API

|                   | Path             | Method | Request data                          | Response data |
|---                |---               |---     |---                                    |---            |
| Server status     | /                | GET    | auth data(username, password)         | string        |
| Files list        | /files           | GET    | auth data(username, password)         | list          |
| Upload a file     | /files           | POST   | auth data(username, password), file   | string        |
| Retrieve a file   | /files/:filename | GET    | auth data(username, password)         | file/stream   |
| Delete a file     | /files/:filename | DELETE | auth data(username, password)         | string        |


### License
pynix-file-server is a free Application:
you can redistribute it and/or modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
pynix-file-server is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 
See COPYING for a copy of the GNU General Public License. If not, see http://www.gnu.org/licenses/.

Copyright (c) 2017 Lahiru Pathirage <http://lahiru.site>
