import sys

from clone_contents import clone_contents
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    base_path = sys.argv[1] if len(sys.argv) == 2 else "/"

    clone_contents(dir_path_static, dir_path_docs)
    generate_pages_recursive(base_path, dir_path_content, template_path, dir_path_docs)


if __name__ == "__main__":
    main()
