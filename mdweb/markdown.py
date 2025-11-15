import sys
import re
import os


class _MDElement:
    def __init__(self, tag, content, attr="", is_void_elem=False):
        self.tag = tag
        self.content = content
        self.attr = attr
        self.is_void_elem = is_void_elem

    def handle_inline(self, text, delim, tag):
        r_delim = re.escape(delim)
        pattern = fr"{r_delim}(.*?){r_delim}"
        return re.sub(pattern, lambda m: f"<{tag}>{m.group(1)}</{tag}>", text)

    def handle_inline_href(self, text):
        pattern = r"\[(.*?)]\((.*?)\)"
        return re.sub(
                pattern,
                lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>',
                text
                )

    def to_html(self):
        if self.is_void_elem:
            if self.attr:
                return f"<{self.tag} {self.attr}>"
            else:
                return f"<{self.tag}>"

        text = self.content
        text = self.handle_inline(text, "**", "strong")
        text = self.handle_inline(text, "__", "strong")
        text = self.handle_inline(text, "_", "em")
        text = self.handle_inline(text, "*", "em")
        text = self.handle_inline(text, "`", "code")
        text = self.handle_inline_href(text)
        if not self.attr:
            html = f"<{self.tag}>{text}</{self.tag}>"
        else:
            html = f"<{self.tag} {self.attr}>{text}</{self.tag}>"
        return html


class MarkdownParser:
    def __init__(self, md_file):
        self.file = md_file
        self.elements = []
        self.__next_line = self.file.readline()
        self.__curr_line = None

    def __get_next_line(self):
        self.__curr_line = self.__next_line
        self.__next_line = self.file.readline()
        return self.__curr_line

    def __peek_line(self):
        return self.__next_line

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

    def __handle_code(self, line):
        return _MDElement("p", line)

    def __get_indent_count(self, line):
        if line is None or line == "":
            return 0
        space_count = 0
        for char in line:
            if char == " ":
                space_count += 1
            else:
                break
        return space_count

    def __get_list_content(self, line):
        if not line:
            return ""
        return " ".join(line.strip().split(" ")[1:])

    def __handle_ul_helper(self, elems, parent_indent):
        nline = self.__peek_line()
        nline_lstrip = nline.lstrip()
        while nline_lstrip.startswith("* ") or nline_lstrip.startswith("- "):
            next_indent = self.__get_indent_count(nline)
            if 0 <= next_indent - parent_indent <= 1:
                self.__get_next_line()
                li_content = self.__get_list_content(self.__curr_line)
                elems.append(_MDElement("li", li_content))
            elif 2 <= next_indent - parent_indent <= 5:
                nested = self.__handle_ul(next_indent)
                nested_content = nested.to_html()
                elems[-1].content += f"\n{nested_content}\n"
            elif next_indent - parent_indent > 5:
                self.__get_next_line()
                elems[-1].content += " " + self.__curr_line.strip()
            else:
                break

            nline = self.__peek_line()
            nline_lstrip = nline.lstrip()

        return elems

    def __handle_ul(self, parent_indent):
        md_list = self.__handle_ul_helper([], parent_indent)
        ul_content = "\n".join([li.to_html() for li in md_list])
        md_ul = _MDElement("ul", f"\n{ul_content}\n")
        return md_ul

    def __handle_ol_helper(self, elems, parent_indent):
        nline = self.__peek_line()
        nline_lstrip = nline.lstrip()
        m = re.match(r"^(\d+)\. (.*)", nline_lstrip)
        while m:
            next_indent = self.__get_indent_count(nline)
            if 0 <= next_indent - parent_indent <= 1:
                self.__get_next_line()
                li_content = self.__get_list_content(self.__curr_line)
                elems.append(_MDElement("li", li_content))
            elif 2 <= next_indent - parent_indent <= 5:
                nested = self.__handle_ol(next_indent)
                nested_content = nested.to_html()
                elems[-1].content += f"\n{nested_content}\n"
            elif next_indent - parent_indent > 5:
                self.__get_next_line()
                elems[-1].content += " " + self.__curr_line.strip()
            else:
                break

            nline = self.__peek_line()
            nline_lstrip = nline.lstrip()
            m = re.match(r"^(\d+)\. (.*)", nline_lstrip)

        return elems

    def __handle_ol(self, parent_indent):
        md_list = self.__handle_ol_helper([], parent_indent)
        ol_content = "\n".join([li.to_html() for li in md_list])
        md_ol = _MDElement("ol", f"\n{ol_content}\n")
        return md_ol

    def __handle_img(self, match):
        alt_text = match.group(1)
        src_n_title = match.group(2)
        m_title = re.search(r'"(.*?)"', src_n_title)
        title = None
        src = None
        if m_title:
            title = m_title.group(1)
            src = re.match(r'^(.*?)\s*', src_n_title).group(1)
            src = src.rstrip()
        else:
            src = src_n_title
        attr = f'src="{src}" alt="{alt_text}"'
        if title is not None:
            attr += f' title="{title}"'
        return _MDElement("img", "", attr, is_void_elem=True)

    def __handle_href(self, match, line):
        front_text = match.group(1)
        href = match.group(2)
        attr = f'href="{href}"'
        return _MDElement("a", front_text, attr)

    def __handle_code_block(self):
        line = self.__get_next_line()
        content = ""
        while self.__peek_line().rstrip() != "```":
            line = self.__get_next_line()
            content += line
        code = _MDElement("code", content).to_html()
        return _MDElement("pre", code)

    def __get_quote(self, line):
        quote_count = 0
        for w in line:
            if w == ">":
                quote_count += 1
            else:
                break
        return quote_count

    def __handle_blockquote_helper(self, elems, parent_quote):
        while self.__peek_line().startswith(">") \
                or self.__peek_line().strip() != "":
            next_quote = self.__get_quote(self.__peek_line())
            if next_quote - parent_quote <= 0:
                nline = self.__peek_line()
                content = nline.lstrip(">").rstrip()
                if content and elems:
                    elems[-1].content += content
                    self.__get_next_line()
                elif content and not elems:
                    line = self.__get_next_line()
                    l_content = line.lstrip(">").lstrip().rstrip()
                    p = _MDElement("p", l_content)
                    elems.append(p)
                elif not content and elems:
                    self.__get_next_line()
                    line = self.__get_next_line()
                    l_content = line.lstrip(">").lstrip().rstrip()
                    p = _MDElement("p", l_content)
                    elems.append(p)
                elif not content and not elems:
                    self.__get_next_line()
                    continue
            else:
                elems.append(self.__handle_blockquote(next_quote))

        return elems

    def __handle_blockquote(self, parent_quote):
        md_p = self.__handle_blockquote_helper([], parent_quote)
        bq_content = "\n".join([p.to_html() for p in md_p])
        md_bq = _MDElement("blockquote", bq_content)
        return md_bq

    def parse(self):
        line = self.__peek_line()
        while line:
            line = line.rstrip()
            if not line:
                # This one will skip empty line
                # Will see if there's more cases need to
                # be handled
                self.__get_next_line()
                line = self.__peek_line()
                continue

            if line.startswith("#"):
                md_header = self.__handle_header(line)
                self.elements.append(md_header)
            elif line.startswith("* ") or line.startswith("- "):
                md_ul = self.__handle_ul(0)
                self.elements.append(md_ul)
            elif line.startswith("**") or line.startswith("__"):
                md_bold = self.__handle_bold(line)
                self.elements.append(md_bold)
            elif line.startswith("*") or line.startswith("_"):
                md_italic = self.__handle_italic(line)
                self.elements.append(md_italic)
            elif line.startswith(">"):
                md_block_quote = self.__handle_blockquote(1)
                self.elements.append(md_block_quote)
            elif line.startswith("```"):
                md_code_block = self.__handle_code_block()
                self.elements.append(md_code_block)
            elif line.startswith("`"):
                md_code = self.__handle_code(line)
                self.elements.append(md_code)
            else:
                m_ol = re.match(r"^(\d+)\. (.*)", line)
                m_img = re.match(r"^!\[(.*)\]\((.*)\)", line)
                m_url = re.match(r"^\[(.*?)]\((.*?)\)", line)
                # TODO (#1): Implement function to get
                # HTML start and type
                if m_ol:
                    md_ol = self.__handle_ol(0)
                    self.elements.append(md_ol)
                elif m_img:
                    md_img = self.__handle_img(m_img)
                    self.elements.append(md_img)
                elif m_url:
                    md_url = self.__handle_href(m_url, line)
                    self.elements.append(md_url)
                else:
                    parag = self.__handle_paragraph(line)
                    self.elements.append(parag)

            self.__get_next_line()
            line = self.__peek_line()

    def generate_template(self, template_content: str):
        """
        Convert parsed elements into HTML and create a new index.html
        file using the template
        """
        if not self.elements:
            return

        elements = [e.to_html() for e in self.elements]
        inserted_content = "\n".join(elements)

        updated_content = template_content.replace(
                "<!--CONTENT-->", inserted_content)

        index_path = "./generated/index.html"
        os.makedirs(os.path.dirname(index_path),
                    exist_ok=True)  # create ./generated if needed
        try:
            with open(index_path, "w") as index_html_file:
                index_html_file.write(updated_content)
        except OSError as e:
            print(f"Failed to write index.html: {e}", file=sys.stderr)

    def dump_element(self):
        for e in self.elements:
            print(e.tag, end=": ")
            print(e.content)

    def dump(self):
        content = self.file.read()
        print(content, end="")
