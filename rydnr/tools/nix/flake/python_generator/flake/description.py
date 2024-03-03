# vim: set fileencoding=utf-8
"""
rydnr/tools/nix/flake/python_generator/flake/description.py

This file defines the Description class.

Copyright (C) 2023-today rydnr's rydnr/python-nix-flake-generator

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from bs4 import BeautifulSoup
import mistune


class Description:
    def extract_html_description(description: str) -> str:
        if description:
            soup = BeautifulSoup(description, "html.parser")
            first_paragraph = soup.find("p")
            if first_paragraph is not None:
                plain_text_description = first_paragraph.get_text()
            else:
                plain_text_description = ""
        else:
            plain_text_description = ""

            return plain_text_description.strip(" \n\t")

    def extract_markdown_description(description: str) -> str:
        if description:
            renderer = mistune.HTMLRenderer()
            parser = mistune.BlockParser(renderer)
            raw_description = extract_html_description(parser.parse(description))
        else:
            raw_description = ""

        return raw_description

    def extract_description(description: str, type: str) -> str:
        if str == "text/html":
            return extract_html_description(str)
        elif str == "text/markdown":
            return extract_markdown_description(str)

        return description


# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
