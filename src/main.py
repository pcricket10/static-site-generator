import os
import shutil
from gencontent import generate_page
from markdown_blocks import markdown_to_html_node
from textnode import TextNode, TextType


def main():

    source = "./static"
    destination = "./public"
    copy_folder_contents(source, destination)

    from_path = "./content/index.md"
    template_path = "./template.html"
    dest_path = "./public/index.html"
    generate_page(from_path, template_path, dest_path)


def copy_folder_contents(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    dir_list = os.listdir(source)
    if dir_list == []:
        return
    for item in dir_list:
        if os.path.isdir(f"{source}/{item}"):
            copy_folder_contents(f"{source}/{item}", f"{destination}/{item}")
        elif os.path.isfile(f"{source}/{item}"):
            shutil.copy(f"{source}/{item}", f"{destination}/{item}")


main()
