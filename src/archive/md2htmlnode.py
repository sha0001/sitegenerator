import md2blocks
import textnode
import htmlnode
import re

def markdown_to_html_node(markdown):
    htmlnodelist = []

    # split markdown into blocks
    blocklist = markdown_to_blocks(markdown)

    # Loop over each block 
    for block in blocklist: 
        bt = block_to_blocktype(block)

        if bt == BlockType.HEAD: 
            hashes = re.findall(r"(.{1,6}#),block")

            tag = f'h{len(hashes[0])+1}'
        

        if bt == BlockType.QUOTE: 
            tag = 'blockquote'

        if bt == BlockType.ULIST: 
            tag = 'ul'

        if bt == BlockType.OLIST: 
            tag = 'ol'

        if bt == BlockType.PARA: 
            tag = 'p'


        if bt == BlockType.CODE: 
            newtn = TextNode(text, TextType.CODE, 
        # skip the next bit, just make a manual text node 
        

        else:
            newtn = TextNode(block,tag)
        
        newhtml = text_node_to_html_node(newtn)


        htmlnodelist.append(HTMLNode(


        def newhtmlnode(HTMLNode): 
            self.tag = block.


        #Determine block type 

        #for block type, create new HTMLNode

        #Assign child HTMLNodes, use text_to_children below

        #don't run codeblocks through text_to_children. Manually create TExtnode and use text_node_to_html_node

# Make all block nodes children to a single parent HTML node <div></div> 




    



