class _MDHeader:
    def __init__(self, tag, content):
        self.tag = tag
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
            return
        content = " ".join(split_line[1:])
        return _MDHeader(header_len, content)

    def parse(self):
        line = self.file.readline()
        while line:
            line = line.rstrip()
            if line.startswith("#"):
                md_header = self.__handle_header(line)
                self.elements.append(md_header)
            else:
                # Handle normal text <p></p>
                pass
            line = self.file.readline()

    def dump_element(self):
        for e in self.elements:
            print(e.tag, end=": ")
            print(e.content)

    def dump(self):
        content = self.file.read()
        print(content, end="")
