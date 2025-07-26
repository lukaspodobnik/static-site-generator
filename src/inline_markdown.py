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
            _split_nodes_delimiter(old_nodes, delimiter, text_type),
        )
    )


def _split_nodes_delimiter(
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
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        for image in images:
            text_parts = text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            text = text_parts[1]
            new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        new_nodes.append(TextNode(text, TextType.TEXT))

    return list(filter(lambda node: node.text != "", new_nodes))


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        for link in links:
            text_parts = text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            text = text_parts[1]
            new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        new_nodes.append(TextNode(text, TextType.TEXT))

    return list(filter(lambda node: node.text != "", new_nodes))


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return findall(r"\[(.*?)\]\((.*?)\)", text)


def text_to_textnodes(text: str) -> list[TextNode]:
    root = TextNode(text, TextType.TEXT)
    textnodes = split_nodes_delimiter([root], "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes
