{
  description = "A Nix flake for python-flake-generator Python package";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix.url = "github:nix-community/poetry2nix";
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ poetry2nix.overlay ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in rec {
        packages = {
          python_nix_flake_generator-0_0_1 =
            (import ./python_nix_flake_generator-0.0.1.nix) {
              inherit (pythonPackages) buildPythonApplication;
              inherit (pkgs) lib;
              mkPoetryApplication = pkgs.poetry2nix.mkPoetryApplication;
            };
          python_nix_flake_generator =
            packages.python_nix_flake_generator-0_0_1;
          default = packages.python_nix_flake_generator;
          meta = with lib; {
            description =
              "A Python CLI application to generate Nix flakes for Python packages";
            license = licenses.gpl3;
            homepage = "https://github.com/rydnr/python-nix-flake-generator";
            maintainers = with maintainers; [ ];
          };
        };
        defaultPackage = packages.default;
        devShell = pkgs.mkShell {
          buildInputs = with pkgs.python3Packages; [ packages.default ];
        };
        shell = flake-utils.lib.mkShell {
          packages = system: [ self.packages.${system}.default ];
        };
      });
}
