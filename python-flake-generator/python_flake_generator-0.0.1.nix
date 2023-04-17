{ buildPythonApplication, lib, mkPoetryApplication }:

let
  projectSrc = mkPoetryApplication {
    projectDir = ./.;
    pname = "python_flake_generator";
    version = "0.0.1";
    pyModule = "python_flake_generator";
  };

in buildPythonApplication rec {
  pname = "python_flake_generator";
  version = "0.0.1";
  format = "pyproject";
  src = projectSrc;

  nativeBuildInputs = [

  ];

  propagatedBuildInputs = [

  ];

  buildInputs = [

  ];

  pythonImportsCheck = [ "python_flake_generator" ];
  meta = with lib; {
    description =
      "A Python CLI application to generate flakes for Python packages";
    license = licenses.gpl3;
    homepage = "https://github.com/rydnr/nix-tools";
    maintainers = with maintainers; [ ];
  };
}
