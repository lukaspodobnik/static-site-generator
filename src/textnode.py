from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (
            self.text == value.text
            and self.text_type == value.text_type
            and self.url == value.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(node: TextNode) -> LeafNode:
    match node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=node.text, props={"href": node.url})
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": node.url, "alt": node.text}
            )
        case _:
            raise ValueError("Given TextNode has bad TextType.")
