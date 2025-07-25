import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_1 = TextNode("This is a text node", TextType.BOLD)
        node_2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node_1, node_2)

        node_1 = TextNode("This is another text node", TextType.LINK, "this-is-url.com")
        node_2 = TextNode("This is another text node", TextType.LINK, "this-is-url.com")
        self.assertEqual(node_1, node_2)

        node_1 = TextNode("This is a text node", TextType.TEXT)
        node_2 = TextNode("This is another one", TextType.TEXT)
        self.assertNotEqual(node_1, node_2)

        node_1 = TextNode("Even another text node!", TextType.IMAGE, "url.com")
        node_2 = TextNode("Even another text node!", TextType.LINK, "url.com")
        self.assertNotEqual(node_1, node_2)

        node_1 = TextNode("Even another text node!", TextType.LINK, "url.com")
        node_2 = TextNode("Even another text node!", TextType.LINK, "url.de")
        self.assertNotEqual(node_1, node_2)


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "link.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="srcisthesrc.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "srcisthesrc.com", "alt": "This is an image node"}
        )

    def test_no_type(self):
        node = TextNode("This is a node with no type.", None)
        self.assertRaises(ValueError, text_node_to_html_node, node)


if __name__ == "main":
    unittest.main()
