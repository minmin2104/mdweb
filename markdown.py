class MarkdownParser:
    def __init__(self, md_file):
        self.file = md_file

    def dump(self):
        content = self.file.read()
        print(content, end="")
