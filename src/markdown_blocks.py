from enum import Enum

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        if block == "":
            continue
        block_list.append(block.strip())
    return block_list


def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.OLIST:
            return olist_to_html_node(block)
        case BlockType.ULIST:
            return ulist_node(block)
        case _:
            raise ValueError("invalid block type")


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)

    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    if not block.startswith("#") or block.startswith("#######"):
        raise ValueError("Error: invalid heading")
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level+1:]
    children = text_to_children(text)

    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.startswith("```"):
        raise ValueError("Error: invalid code block")

    text = block[4: -3]
    children = text_node_to_html_node(TextNode(text, TextType.TEXT))
    code = ParentNode("code", [children])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines_list = []
    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Error: invalid quote")
        lines_list.append(line[2:])
    text = " ".join(lines_list)
    children = text_to_children(text)

    return ParentNode("blockquote", children)


def olist_to_html_node(block):
    child_lines = []
    lines = block.split("\n")
    for line in lines:
        stripped_line = line.split(". ")[1]
        children = text_to_children(stripped_line)
        child_lines.append(ParentNode("li", children))
    return ParentNode("ol", child_lines)


def ulist_node(block):
    child_lines = []
    lines = block.split("\n")
    for line in lines:
        stripped_line = line[2:]
        children = text_to_children(stripped_line)
        child_lines.append(ParentNode("li", children))
    return ParentNode("ul", child_lines)
