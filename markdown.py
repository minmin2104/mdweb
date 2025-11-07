import sys


class _MDElement:
    def __init__(self, tag, content):
        self.tag = tag
        self.content = content

    def to_html(self):
        return f"<{self.tag}>{self.content}</{self.tag}>"


class MarkdownParser:
    def __init__(self, md_file):
        self.file = md_file
        self.elements = []

    def __handle_header(self, line):
        split_line = line.split(" ")
        header = split_line[0]
        header_len = len(header)
        if header_len > 6:
            return _MDElement("p", line)
        content = " ".join(split_line[1:])
        return _MDElement(f"h{header_len}", content)

    def __handle_paragraph(self, line):
        return _MDElement("p", line)

    def parse(self):
        line = self.file.readline()
        while line:
            line = line.rstrip()
            if line.startswith("#"):
                md_header = self.__handle_header(line)
                self.elements.append(md_header)
            elif line.startswith(""):
                # Suppose to skip empty line
                # Gonna see if there's more cases to handle
                line = self.file.readline()
                continue
            else:
                parag = self.__handle_paragraph(line)
                self.elements.append(parag)

            line = self.file.readline()

    def generate_template(self, template_filepath):
        """
        Convert parsed elements into HTML and create a new index.html
        file using the template
        """
        if not self.elements:
            return

        template_file = None
        try:
            template_file = open(template_filepath, "r+")
        except OSError as e:
            print(f"Failed to read template: {e}", file=sys.stderr)
            return

        inserted_content = ""
        for e in self.elements:
            txt = e.to_html()
            inserted_content += f"{txt}\n"

        original_content = template_file.read()
        template_file.close()
        updated_content = original_content.replace(
                "<!--CONTENT-->",
                inserted_content
                )
        index_html_file = None
        index_path = "generated/index.html"
        try:
            index_html_file = open(index_path, "w")
        except OSError as e:
            print(f"Failed to write index.html: {e}", file=sys.stderr)
            return

        index_html_file.write(updated_content)
        index_html_file.close()

    def dump_element(self):
        for e in self.elements:
            print(e.tag, end=": ")
            print(e.content)

    def dump(self):
        content = self.file.read()
        print(content, end="")
