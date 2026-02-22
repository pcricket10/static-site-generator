def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    block_list = []
    for block in blocks:
        if block == "":
            continue
        block_list.append(block.strip())
    return block_list
