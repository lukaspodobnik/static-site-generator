import re

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown: str):
    div = ParentNode(tag="div", children=[])

    for block in markdown_to_blocks(markdown):
        parent_node: ParentNode

        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                parent_node = _make_paragraph(block)
            case BlockType.HEADING:
                parent_node = _make_heading(block)
            case BlockType.QUOTE:
                parent_node = _make_quote(block)
            case BlockType.CODE:
                parent_node = _make_code(block)
            case BlockType.UNORDERED_LIST:
                parent_node = _make_unordered_list(block)
            case BlockType.ORDERED_LIST:
                parent_node = _make_ordered_list(block)

        div.children.append(parent_node)

    return div


def _make_paragraph(block: str) -> ParentNode:
    return ParentNode(
        tag="p",
        children=_text_to_children(block.replace("\n", " ")),
    )


def _make_heading(block: str) -> ParentNode:
    match re.match(r"#{1,6}", block).group():
        case "#":
            num = 1
        case "##":
            num = 2
        case "###":
            num = 3
        case "####":
            num = 4
        case "#####":
            num = 5
        case "######":
            num = 6

    return ParentNode(tag=f"h{num}", children=_text_to_children(block[num + 1 :]))


def _make_quote(block: str) -> ParentNode:
    return ParentNode(
        tag="blockquote",
        children=_text_to_children(
            "\n".join(line[1:] for line in block.split("\n")).replace("\n", " ")
        ),
    )


def _make_code(block: str) -> ParentNode:
    return ParentNode(
        tag="pre", children=[LeafNode(tag="code", value=block[3:-3].lstrip(" \n"))]
    )


def _make_unordered_list(block: str) -> ParentNode:
    return ParentNode(
        tag="ul",
        children=[
            ParentNode(tag="li", children=_text_to_children(line[2:]))
            for line in block.strip(" \n").split("\n")
        ],
    )


def _make_ordered_list(block: str) -> ParentNode:
    return ParentNode(
        tag="ol",
        children=[
            ParentNode(tag="li", children=_text_to_children(line[3:]))
            for line in block.strip(" \n").split("\n")
        ],
    )


def _text_to_children(text: str) -> list[LeafNode]:
    return [text_node_to_html_node(text_node) for text_node in text_to_textnodes(text)]
