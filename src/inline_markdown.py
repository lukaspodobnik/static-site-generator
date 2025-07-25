from re import findall

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    if text_type == TextType.TEXT:
        raise ValueError("This function only takes BOLD, ITALIC or CODE for text_tpye.")

    if delimiter is None or delimiter == "" or delimiter == " ":
        raise ValueError("Not a valid delimiter.")

    return list(
        filter(
            lambda node: node.text != "",
            __split_nodes_delimiter(old_nodes, delimiter, text_type),
        )
    )


def __split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text_parts = node.text.split(delimiter, maxsplit=2)
        if len(text_parts) == 1:
            new_nodes.append(node)

        elif len(text_parts) == 3:
            sub_nodes_pre = split_nodes_delimiter(
                [TextNode(text_parts[0], TextType.TEXT)], delimiter, text_type
            )
            sub_nodes_post = split_nodes_delimiter(
                [TextNode(text_parts[2], TextType.TEXT)], delimiter, text_type
            )

            new_nodes.extend(sub_nodes_pre)
            new_nodes.append(TextNode(text_parts[1], text_type))
            new_nodes.extend(sub_nodes_post)

        else:
            raise Exception(
                "Invalid Markdown syntax (likely missing a closing delimiter)."
            )

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    pass


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    pass


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return findall(r"\[(.*?)\]\((.*?)\)", text)
