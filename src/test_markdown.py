from .markdown import _MDElement as MDElement
import unittest


class TestInlineHandler(unittest.TestCase):
    def test_inline_handler(self):
        text = "abc *def ghi* jkl *mno*"
        md_element = MDElement("em", text)
        actual = md_element.handle_inline_re()
        expected = "abc <em>def ghi</em> jkl <em>mno</em>"
        self.assertTrue(actual == expected)


if __name__ == "__main__":
    unittest.main()
