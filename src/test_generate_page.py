import unittest

from generate_page import extract_title


class TestExtractHeader(unittest.TestCase):
    def test_startswith_header(self):
        md = """
# Header
Text text text
"""
        self.assertEqual(extract_title(md), "Header")

    def test_header_in_middle(self):
        md = """
Text before header
# Header
Text text text
"""
        self.assertEqual(extract_title(md), "Header")

    def test_no_valid_header(self):
        md = """
#Header
Text text text
"""
        self.assertRaises(Exception, extract_title, md)
