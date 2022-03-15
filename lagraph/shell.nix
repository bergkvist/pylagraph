{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/33da2dcc496668974369e15667db2c47e2dde6b7.tar.gz") {}
, python ? pkgs.python38
}:
pkgs.mkShell {
  buildInputs = [
    python
    python.pkgs.wheel
    python.pkgs.setuptools
    python.pkgs.twine
  ];
}