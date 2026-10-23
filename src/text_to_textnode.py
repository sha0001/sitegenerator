from split import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

def text_to_textnodes(text): 
    plain = [TextNode(text, TextType.TEXT)]
    print(f'plain={plain}')

    boldsplit = split_nodes_delimiter(plain, '**', TextType.BOLD)
    print(f'boldsplit={boldsplit}')
    
    italicsplit = split_nodes_delimiter(boldsplit, '_', TextType.ITALIC)
    print(f'italic={italicsplit}')

    codesplit = split_nodes_delimiter(italicsplit, '`', TextType.CODE)

    imagesplit = split_nodes_image(codesplit)

    linksplit = split_nodes_link(imagesplit)

    print(f'linksplit={linksplit}')
    return linksplit

