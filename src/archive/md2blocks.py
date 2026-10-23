
def markdown_to_blocks(markdown): 
    splitmd = markdown.split("\n\n")
    
    blocklist = []
    for block in splitmd: 
        block = block.strip()
        if block: 
            blocklist.append(block)

    return blocklist



