with import <nixpkgs> {};

# Preare Python environment
(
    pkgs.python35.buildEnv.override rec {
        extraLibs = [ pkgs.python35Packages.flask pkgs.python35Packages.pyyaml ];
    }

).env