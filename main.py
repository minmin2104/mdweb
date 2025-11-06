from markdown import MarkdownParser
import sys
import os


class Main:
    def __init__(self, filepath):
        self.filepath = filepath
        if not self.__is_file_md():
            print("Error: File is not a Markdown File", file=sys.stderr)
            return

        self.file = None
        try:
            self.file = open(self.filepath)
        except OSError as e:
            print(f"Failed to open {self.filepath}: {e}", file=sys.stderr)
            return

        md_parser = MarkdownParser(self.file)
        md_parser.dump()

    def __is_file_md(self):
        if os.path.basename(self.filepath).split(".")[1] == "md":
            return True
        return False


if __name__ == "__main__":
    filepath = "./README.md"
    main = Main(filepath)
