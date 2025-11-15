from .markdown import MarkdownParser
from importlib import resources
import argparse
import shutil
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
        md_parser.parse()
        # md_parser.dump_element()

        template_html = resources.read_text("mdweb.template", "template.html")
        md_parser.generate_template(template_html)

        css_content = resources.read_text("mdweb.template", "style.css")
        os.makedirs("./generated", exist_ok=True)
        with open("./generated/style.css", "w") as css_file:
            css_file.write(css_content)

        self.file.close()

    def __is_file_md(self):
        if os.path.basename(self.filepath).split(".")[1] == "md":
            return True
        return False


def main():
    parser = argparse.ArgumentParser(
            "mdweb",
            description="Transform text written\
                    in Markdown into static webpages"
            )
    parser.add_argument("dir", help="Directory containing index.md")
    args = parser.parse_args()
    path = args.dir
    filepath = f"{path}/index.md"
    Main(filepath)
    dst = "./generated"
    shutil.copytree(path, dst, ignore=shutil.ignore_patterns("index.md"),
                    dirs_exist_ok=True)


if __name__ == "__main__":
    main()
