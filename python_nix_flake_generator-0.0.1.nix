{ buildPythonApplication, lib, mkPoetryApplication }:

mkPoetryApplication rec {
  pname = "python_nix_flake_generator";
  version = "0.0.1";
  format = "pyproject";
  projectDir = ./.;

  nativeBuildInputs = [ ];

  propagatedBuildInputs = [ ];

  buildInputs = [ ];

  pythonImportsCheck = [ ];
  meta = with lib; {
    description =
      "A Python CLI application to generate Nix flakes for Python packages";
    license = licenses.gpl3;
    homepage = "https://github.com/rydnr/python-nix-flakes-generator";
    maintainers = with maintainers; [ ];
  };
}
