import os
import shutil
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


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            stripped_line = line[2:].strip()
            return stripped_line
    raise Exception("no h1 header")


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file_contents = ""
    template_file_contents = ""
    html_string = ""
    if os.path.exists(from_path):
        with open(from_path) as f:
            markdown_file_contents = f.read()
    if os.path.exists(template_path):
        with open(template_path) as f:
            template_file_contents = f.read()

    content = markdown_to_html_node(markdown_file_contents).to_html()
    title = extract_title(markdown_file_contents)
    dest_file_contents = template_file_contents.replace(
        "{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, "w") as f:
        f.write(dest_file_contents)


main()
