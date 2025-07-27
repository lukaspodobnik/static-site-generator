import os

from markdown_to_html_node import markdown_to_html_node


def extract_title(markdown: str) -> str:
    h1_headers = list(filter(lambda line: line.startswith("# "), markdown.split("\n")))
    if len(h1_headers) == 0:
        raise Exception("Markdown has no header (# ).")
    return h1_headers[0][2:]


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    if not os.path.isfile(from_path):
        raise FileNotFoundError(f"from_path: {from_path} not found.")
    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"template_path: {template_path} not found.")

    with open(from_path, "r") as f:
        md = f.read()

    with open(template_path, "r") as f:
        html = f.read()

    title = extract_title(md)
    content = markdown_to_html_node(md).to_html()
    html = html.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)

    with open(dest_path, "w") as f:
        f.write(html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for name in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, name)
        if os.path.isfile(src_path):
            generate_page(
                src_path,
                template_path,
                os.path.join(dest_dir_path, name.rstrip(".md") + ".html"),
            )
        else:
            dst_path = os.path.join(dest_dir_path, name)
            os.mkdir(dst_path)
            generate_pages_recursive(src_path, template_path, dst_path)
