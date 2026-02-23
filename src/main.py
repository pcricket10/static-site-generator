from textnode import TextNode, TextType


def main():
    text = "This is a text node"
    text_type = TextType.BOLD
    url = "https://www.boot.dev"

    text_node = TextNode(text, text_type, url)
    print(text_node)

# def copy_folder_contents(source, destination):


main()
