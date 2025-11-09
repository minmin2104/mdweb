import sys
import re
import os


class _MDElement:
    def __init__(self, tag, content):
        self.tag = tag
        self.content = content

    def __replacer_tag(self):
        def replacer(match):
            return f"<{self.tag}>{match.group(1)}</{self.tag}>"
        return replacer

    def handle_inline(self, text, delim, tag):
        r_delim = re.escape(delim)
        pattern = fr"{r_delim}(.*?){r_delim}"
        return re.sub(pattern, lambda m: f"<{tag}>{m.group(1)}</{tag}>", text)

    def to_html(self):
        text = self.content
        text = self.handle_inline(text, "**", "strong")
        text = self.handle_inline(text, "__", "strong")
        text = self.handle_inline(text, "_", "em")
        text = self.handle_inline(text, "*", "em")
        return f"<{self.tag}>{text}</{self.tag}>"


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

    def __handle_italic(self, line):
        return _MDElement("p", line)

    def __handle_bold(self, line):
        return _MDElement("p", line)

    def __handle_unordered_list(self, line):
        li = []
        while line.startswith("* ") or line.startswith("- "):
            line = line.rstrip()
            li_content = " ".join(line.split(" ")[1:])
            li_element = _MDElement("li", li_content)
            li.append(li_element.to_html())
            line = self.file.readline()
            nested_li = []
            while line.startswith("    * ") or line.startswith("    - "):
                line = line.rstrip()
                li_content = " ".join(line.split(" ")[5:])
                nest_li_element = _MDElement("li", li_content)
                nested_li.append(nest_li_element.to_html())
                line = self.file.readline()
            if nested_li:
                last_li = li[-1]
                nested_ul = "\n".join(nested_li)
                print(nested_ul)
                nested_ul_elem = _MDElement("ul", nested_ul)
                li[-1] = last_li.replace("</li>",
                                         f"{nested_ul_elem.to_html()}</li>")
        ul = "\n".join(li)
        ul_element = _MDElement("ul", ul)
        return ul_element, line

    def parse(self):
        line = self.file.readline()
        while line:
            line = line.rstrip()
            if not line:
                # This one will skip empty line
                # Will see if there's more cases need to
                # be handled
                line = self.file.readline()
                continue

            if line.startswith("#"):
                md_header = self.__handle_header(line)
                self.elements.append(md_header)
            elif line.startswith("* ") or line.startswith("- "):
                md_ul, line = self.__handle_unordered_list(line)
                self.elements.append(md_ul)
            elif line.startswith("**") or line.startswith("__"):
                md_bold = self.__handle_bold(line)
                self.elements.append(md_bold)
            elif line.startswith("*") or line.startswith("_"):
                # TODO (#2): Handle unordered list for '*'
                md_italic = self.__handle_italic(line)
                self.elements.append(md_italic)
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
        index_path = "./generated/index.html"
        os.makedirs(os.path.dirname(index_path),
                    exist_ok=True)  # create ./generated if needed
        try:
            index_html_file = open(index_path, "w")
        except OSError as e:
            print(f"Failed to write index.html: {e}", file=sys.stderr)
            return
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
