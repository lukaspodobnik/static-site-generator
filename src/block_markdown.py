from enum import Enum
from functools import reduce
from re import match


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown: str):
    return list(
        filter(lambda block: block != "", map(str.strip, markdown.split("\n\n")))
    )


def block_to_block_type(block: str) -> BlockType:
    if match(r"#{1,6} ", block):
        return BlockType.HEADING

    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    elif reduce(
        lambda acc, x: acc and x,
        map(lambda line: line.startswith(">"), block.split("\n")),
    ):
        return BlockType.QUOTE

    elif reduce(
        lambda acc, x: acc and x,
        map(lambda line: line.startswith("- "), block.split("\n")),
    ):
        return BlockType.UNORDERED_LIST

    elif reduce(
        lambda acc, x: acc and x,
        map(
            lambda x: x[1].startswith(str(x[0] + 1) + ". "),
            enumerate(block.split("\n")),
        ),
    ):
        return BlockType.ORDERED_LIST

    else:
        return BlockType.PARAGRAPH
