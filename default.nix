with import <nixpkgs> {};


let
    buildInputs = [
        nginx
        python35Packages.python
        python35Packages.flask
        python35Packages.pyyaml
    ];

in {
    network.description = "Local machine";

    webserver = {
        deployment = {
            targetEnv = "virtualbox";
            targetHost = "192.168.56.1";
            virtualbox.memorySize = 1024;
        };

            services = {
            nginx = {
                enable = true;
                config = '';
                    http {
                        include         ${nginx}/conf/mime.types;
                        server_name     localhost;

                        location / {
                            proxy_pass http://localhost:5000;
                        }
                    }
                '';
            };
        };
    };
}

