import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(
            props={
                "href": "https://www.google.com",
            }
        )
        self.assertEqual(html_node.props_to_html(), ' href="https://www.google.com"')

        html_node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            html_node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

        html_node = HTMLNode(props=None)
        self.assertEqual(html_node.props_to_html(), "")

        html_node = HTMLNode(props={})
        self.assertEqual(html_node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", props={"href": "the_link.com"})
        self.assertEqual(node.to_html(), '<a href="the_link.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is plain text")
        self.assertEqual(node.to_html(), "This is plain text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("p", None)
        self.assertRaises(ValueError, parent_node.to_html)

        parent_node = ParentNode("p", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_multiple_children(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode(None, "Normal")
        parent_node = ParentNode("p", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold</b>Normal</p>")
