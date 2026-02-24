import os

from markdown_blocks import markdown_to_html_node


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


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            stripped_line = line[2:].strip()
            return stripped_line
    raise Exception("no h1 header")
