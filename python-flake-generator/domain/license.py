#!/usr/bin/env python3

class License():
    def pypi_license_to_nix_license(pypi_license: str) -> str:
        license_map = {
            "Apache-2.0": "asl20",
            "MIT": "mit",
            "GPL-3.0": "gpl3",
            "GPL-3.0+": "gpl3Plus",
            "LGPL-3.0": "lgpl3",
            "LGPL-3.0+": "lgpl3Plus",
            "BSD-2-Clause": "bsd2",
            "BSD-3-Clause": "bsd3",
        }

        nix_license = license_map.get(pypi_license)

        if not nix_license:
            # raise ValueError(f"Unknown PyPI license: {pypi_license}")
            nix_license = "mit"

        return nix_license
