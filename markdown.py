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

    def dump_element(self):
        for e in self.elements:
            print(e.tag, end=": ")
            print(e.content)

    def dump(self):
        content = self.file.read()
        print(content, end="")
