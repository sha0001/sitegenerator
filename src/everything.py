import re
from enum import Enum

###### CLASSES 

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold" 
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image" 


class BlockType(Enum): 
    PARA = "paragraph" 
    HEAD = "heading" 
    CODE = "code" 
    QUOTE = "quote" 
    ULIST = "unordered list" 
    OLIST = "ordered_list" 


class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text =text 
        self.text_type = text_type
        self.url = url
    
    def __eq__(self,other): 
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self): 
        return f'TextNode({self.text}, {self.text_type}, {self.url})' 

class HTMLnode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None or self.props =={}:
            return []
        else: 
            return f'href="{self.props["href"]}" target="{self.props["target"]}"'

    def __repr__(self):
        return f'tag = {self.tag} value ={self.value} children = {self.children} props = {self.props}'


class LeafNode(HTMLnode): 
    def __init__(self,tag,value,props=None): 
        self.tag = tag
        self.value = value 
        self.props = props 

    def to_html(self): 
        if not self.value: 
            raise ValueError
        if not self.tag: 
            return str(self.value)
        if self.props==None: 
            return f'<{self.tag}>{self.value}</{self.tag}>'

        return f'<{self.tag} href="{self.props["href"]}">{self.value}</{self.tag}>'

    def __repr__(self): 
        return f'tag = {self.tag} value ={self.value} props = {self.props}'


class ParentNode(HTMLnode): 
    def __init__(self,tag,children,props=None): 
        self.tag = tag 
        self.children = children 
        self.props = props

    def to_html(self): 
        if not self.tag: 
            raise ValueError('no tag')
        
        if not self.children: 
            raise ValueError('no children')
       
        htmlout = ''
        
        for child in self.children: 
            htmlout+= child.to_html()
        
        if self.props == None: 
            return f'<{self.tag}>{htmlout}</{self.tag}>'

        return f'<{self.tag} href="{self.props["href"]}">{htmlout}</{self.tag}>'


####### FUNCTIONS


def extract_markdown_images(text): 
    return re.findall(r"\!\[(.*?)\]\((.*?)(?=\))",text) 

def extract_markdown_links(text): 
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)(?=\))",text)


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

def text_to_textnodes(text): 
    plain = [TextNode(text, TextType.TEXT)]

    boldsplit = split_nodes_delimiter(plain, '**', TextType.BOLD)
    
    italicsplit = split_nodes_delimiter(boldsplit, '_', TextType.ITALIC)

    codesplit = split_nodes_delimiter(italicsplit, '`', TextType.CODE)

    imagesplit = split_nodes_image(codesplit)

    linksplit = split_nodes_link(imagesplit)

    return linksplit



def text_node_to_html_node(text_node: TextNode) -> LeafNode: 
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None,text_node.text)
    if text_node.text_type == TextType.BOLD: 
        return LeafNode('b',text_node.text)
    if text_node.text_type == TextType.ITALIC: 
        return LeafNode('i',text_node.text)
    if text_node.text_type == TextType.CODE: 
        return LeafNode('code',text_node.text)
    if text_node.text_type == TextType.LINK: 
        return LeafNode('a',text_node.value)
    if text_node.text_type == TextType.IMAGE: 
        return LeafNode('img','',{src: text_node.url, alt: text_node.props['alt']})


def markdown_to_blocks(markdown): 
    splitmd = markdown.split("\n\n")
    
    blocklist = []
    for block in splitmd: 
        block = block.strip()
        if block: 
            blocklist.append(block)

    return blocklist

def block_to_block_type(block): 
    
    # 0-6# ... \n 
    if re.findall(r"(.{1,6}#) (.*)",block): 
        return BlockType.HEAD

    # ```\n ... ```
    if re.findall(r"```\n[\s\S]*```",block):
        return BlockType.CODE

    # > ...
    if re.findall(r">\s?(.*)",block):
        return BlockType.QUOTE

    # - 
    if re.findall(r"- (.*)",block):
        return BlockType.ULIST

    # 1.
    # Not bothering to check whether numbering is correct at this point
    if re.findall(r"\d. (.*)",block): 
        return BlockType.OLIST

    else:
        return BlockType.PARA


def markdown_to_html_node(markdown):
    htmlnodelist = []

    # split markdown into blocks
    blocklist = markdown_to_blocks(markdown)

    # Loop over each block 
    for block in blocklist:

        #find block type
        bt = block_to_blocktype(block)

        if bt == BlockType.CODE: 
            #call helper function
            
            #remove code markers
            stripped_block = re.findall(r"```[\s](.*)[\s]",block)
            textnodelist.append(TextNode(stripped_block,TextType.CODE)

        if bt == BlockType.HEAD:            
            node = heading_to_html_node(block)

        if bt == BlockType.QUOTE: 
            node = quote_to_html_node(block)

        if bt == BlockType.ULIST: 
            node = ulist_to_html_node(block)

        if bt == BlockType.OLIST: 
            node = olist_to_html_node(block)

        if bt == BlockType.PARA: 
            node = para_to_html_node(block)
    

        htmlnodelist.append(node)


    return ParentNode('div'

        #Assign child HTMLNodes, use text_to_children below

        #don't run codeblocks through text_to_children. Manually create TExtnode and use text_node_to_html_node

# Make all block nodes children to a single parent HTML node <div></div> 




### Boots says these sub function make the whole thing easier to understand. Makes sense.

def para_to_html_node(block): 
    #tag = 'p'
    return

def olist_to_html_node(block):
    #tag = 'ol'
    return

def ulist_to_html_node(block):
    #tag = 'ul'
    return

def quote_to_html_node(block):
    #tag = 'blockquote'
    return

def heading_to_html_node(block):
    return
    

    # the regex check below is apparently not great. Just use a normal loop instead. 
    # count hashes
    #hashes = re.findall(r"(?<!.)\s*(#{1,6}),block")
    #hashcount = len(hashes)+1        
    #tag = f'h{hashcount}'
    # remove hashes
    #stripped_block = re.findall(r"#{1,6}(.*)",block)

