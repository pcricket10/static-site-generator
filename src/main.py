import os
import shutil
import sys
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

static_path = "./static"
public_path = "./docs"
content_path = "./content"
template_path = "./template.html"
basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]


def main():
    print("Deleting public directory...")
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    print("Copying static files to public directory...")
    copy_files_recursive(static_path, public_path)

    print("Generating page...")
    generate_pages_recursive(
        content_path, template_path, public_path, basepath="/")


main()
