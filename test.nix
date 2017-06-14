# Preare default Python testing environment

with import <nixpkgs> {};


(
    pkgs.python35.buildEnv.override rec {
        extraLibs = [
            pkgs.python35Packages.flask
            pkgs.python35Packages.flask_testing
            pkgs.python35Packages.pyyaml
            pkgs.python35Packages.requests
        ];
    }

).env