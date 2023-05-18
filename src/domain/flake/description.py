from bs4 import BeautifulSoup
import mistune

class Description():

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
        if (str == 'text/html'):
            return extract_html_description(str)
        elif (str == 'text/markdown'):
            return extract_markdown_description(str)

        return description
