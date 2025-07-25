import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_plain_text(self):
        node = TextNode("This is plain text.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, [node])

    def test_single_bold_1_part(self):
        node = TextNode("**This is bold.**", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, [TextNode("This is bold.", TextType.BOLD)])

    def test_single_bold_2_parts(self):
        node = TextNode("**This is** bold.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [TextNode("This is", TextType.BOLD), TextNode(" bold.", TextType.TEXT)],
        )

        node = TextNode("This is **bold.**", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [TextNode("This is ", TextType.TEXT), TextNode("bold.", TextType.BOLD)],
        )

    def test_single_bold_3_parts(self):
        node = TextNode("This is **bold**.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_multiple_bold(self):
        node = TextNode("This is **bold**, and this is also **bold**.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", and this is also ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_multiple_italic(self):
        node = TextNode(
            "This is __italic__, and this is also __italic__.", TextType.TEXT
        )
        split_nodes = split_nodes_delimiter([node], "__", TextType.ITALIC)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and this is also ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_multiple_code(self):
        node = TextNode("This is `code`, and this is also `code`.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(", and this is also ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_no_bold(self):
        node = TextNode("This text has no __bold__", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(split_nodes, [node])

    def test_mixed_on_bold(self):
        node = TextNode("This is **bold** and this is __italic__.", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and this is __italic__.", TextType.TEXT),
            ],
        )

    def test_mixed_full(self):
        node = TextNode(
            "This text has **bold**, **second bold**, __italic__ and `code`.",
            TextType.TEXT,
        )
        split_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        split_nodes = split_nodes_delimiter(split_nodes, "__", TextType.ITALIC)
        split_nodes = split_nodes_delimiter(split_nodes, "`", TextType.CODE)
        self.assertEqual(
            split_nodes,
            [
                TextNode("This text has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("second bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT),
            ],
        )


class TestExtractMarkdownImagesAndLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_mardown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://l.link)")
        self.assertListEqual([("link", "https://l.link")], matches)
