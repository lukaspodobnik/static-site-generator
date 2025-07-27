from clone_contents import clone_contents
from generate_page import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    clone_contents(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
