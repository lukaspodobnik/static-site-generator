import unittest

from textnode import TextNode, TextType


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


if __name__ == "main":
    unittest.main()
