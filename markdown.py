class _MDHeader:
    def __init__(self, tag, content):
        self.tag = tag
        self.content = content


class _MDParagraph:
    def __init__(self, content):
        self.tag = "p"
        self.content = content


class MarkdownParser:
    def __init__(self, md_file):
        self.file = md_file
        self.elements = []

    def __handle_header(self, line):
        split_line = line.split(" ")
        header = split_line[0]
        header_len = len(header)
        if header_len > 6:
            return _MDParagraph(line)
        content = " ".join(split_line[1:])
        return _MDHeader(f"h{header_len}", content)

    def __handle_paragraph(self, line):
        return _MDParagraph(line)

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
