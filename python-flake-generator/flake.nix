{
  description = "A Nix flake for python-flake-generator Python package";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = inputs:
    with inputs;
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in rec {
        packages = {
          python_flake_generator-0_0_1 =
            (import ./python_flake_generator-0.0.1.nix) {
              inherit (pythonPackages) buildPythonPackage setuptools;
              inherit (pkgs) lib;
            };
          python_flake_generator = packages.python_flake_generator-0_0_1;
          default = packages.python_flake_generator;
          meta = with lib; {
            description =
              "A Python CLI application to generate flakes for Python packages";
            license = licenses.gplv3;
            homepage = "https://github.com/rydnr/nix-tools";
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
