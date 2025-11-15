from markdown import MarkdownParser
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

        template_path = "./template/template.html"
        md_parser.generate_template(template_path)

        css_template = "./template/style.css"
        shutil.copy(css_template, "./generated/style.css")

        self.file.close()

    def __is_file_md(self):
        if os.path.basename(self.filepath).split(".")[1] == "md":
            return True
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            "mdweb",
            description="Transform text written\
                    in Markdown into static webpages"
            )
    parser.add_argument("dir", help="Directory containing index.md")
    args = parser.parse_args()
    path = args.dir
    filepath = f"{path}/index.md"
    main = Main(filepath)
    dst = "./generated"
    shutil.copytree(path, dst, ignore=shutil.ignore_patterns("index.md"),
                    dirs_exist_ok=True)
