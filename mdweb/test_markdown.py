import unittest
from .markdown import _MDElement as MDElement


class TestInlineHandler(unittest.TestCase):
    def test_inline_handler(self):
        test_cases = [
                ("abc *def ghi* jkl *mno*", "*", "em",
                 "abc <em>def ghi</em> jkl <em>mno</em>"),
                ("abc _def ghi_ jkl _mno_", "_", "em",
                 "abc <em>def ghi</em> jkl <em>mno</em>"),
                ("abc **bold** jkl **strong**", "**", "strong",
                 "abc <strong>bold</strong> jkl <strong>strong</strong>"),
                ("abc __bold__ jkl __strong__", "__", "strong",
                 "abc <strong>bold</strong> jkl <strong>strong</strong>"),
                ("abc __*bold*__ jkl __*strong*__", "__", "strong",
                 "abc <strong>*bold*</strong> jkl <strong>*strong*</strong>"),
                ("abc <strong>*bold*</strong> jkl <strong>*strong*</strong>",
                 "*", "em",
                 "abc <strong><em>bold</em></strong> jkl\
 <strong><em>strong</em></strong>"),
                ]

        for text, delim, tag, expected in test_cases:
            """
            The tag for MDElement supposed to be "p" but for simplicity
            we just use `tag` variable because it's not relevant in this test
            """
            md_element = MDElement(tag, text)
            actual = md_element.handle_inline(text, delim, tag)
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
