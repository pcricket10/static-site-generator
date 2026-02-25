import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive

static_path = "./static"
public_path = "./public"
content_path = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print("Copying static files to public directory...")
    copy_files_recursive(static_path, public_path)

    print("Generating page...")
    generate_pages_recursive(content_path, template_path, public_path)


main()
