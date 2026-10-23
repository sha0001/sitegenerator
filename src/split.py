
from textnode import TextType, TextNode
from extract import extract_markdown_images
from extract import extract_markdown_links

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]: 
    new_nodes = []
    for node in old_nodes:
        typed_node = []
        if node.text_type != TextType.TEXT:
            typed_node = [node]
            new_nodes.extend(typed_node)


        else: 
            split_node = node.text.split(delimiter) 
            #if len(split_node) < 3: 
             #   raise Exception('not valid markdown') 
            for i in range(0,len(split_node)): 
                if i%2 == 0: 
                    typed_node.append(TextNode(split_node[i], TextType.TEXT))
                else: 
                    typed_node.append(TextNode(split_node[i], text_type) )

            new_nodes.extend(typed_node)
    return new_nodes



def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]: 
    new_nodes = [] 
    
    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            typed_node = [node]
            new_nodes.extend(typed_node)
            continue

        images = extract_markdown_images(node.text)
        
        node_text = node.text
        
        text_list = []
        
        for image in images:

            split = node_text.split(f'![{image[0]}]({image[1]})')
            
            new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0],TextType.IMAGE, image[1]))
            

            node_text = f'{split[1]}'
        
        if node_text: 
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            continue

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]: 
    new_nodes = []

    for node in old_nodes: 
        if node.text_type != TextType.TEXT:
            typed_node = [node]
            new_nodes.extend(typed_node)
            continue
        links = extract_markdown_links(node.text)

        node_text = node.text

        text_list = []

        for link in links:
            split = node_text.split(f'[{link[0]}]({link[1]})')
            
            new_nodes.append(TextNode(split[0],TextType.TEXT)) 
            new_nodes.append(TextNode(link[0],TextType.LINK, link[1]))
            node_text = f'{split[1]}'
        if node_text: 
            new_nodes.append(TextNode(node_text, TextType.TEXT))
            continue

    return new_nodes


    links = extract_markdown_links(node.text)
