import unittest

from markdown_to_html_node import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_heading_plain(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

    def test_heading_with_bold(self):
        md = "### Heading **3**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>Heading <b>3</b></h3></div>")

    def test_quote(self):
        md = """
>quote1
>quote2
>quote3

>quote4
>quote5
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quote1 quote2 quote3</blockquote><blockquote>quote4 quote5</blockquote></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item
- Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item with **bold** text
2. Second item with _italic_ text
3. Third item with `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item with <b>bold</b> text</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code></li></ol></div>",
        )

    def test_full_example_page(self):
        pass
