from enum import Enum
from htmlnode import LeafNode
from htmlnode import HTMLnode
from htmlnode import ParentNode
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold" 
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image" 

class TextNode:
    def __init__(self,text,text_type,url=None):
        self.text =text 
        self.text_type = text_type
        self.url = url
    
    def __eq__(self,other): 
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self): 
        return f'TextNode({self.text}, {self.text_type}, {self.url})' 

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


class BlockType(Enum): 
    PARA = "paragraph" 
    HEAD = "heading" 
    CODE = "code" 
    QUOTE = "quote" 
    ULIST = "unordered list" 
    OLIST = "ordered_list" 


def block_to_block_type(markdown): 
    
    # 0-6# ... \n 
    if re.findall(r"(.{1,6}#) (.*)",markdown): 
        return BlockType.HEAD

    # ```\n ... ```
    if re.findall(r"```\n[\s\S]*```",markdown):
        return BlockType.CODE

    # > ...
    if re.findall(r">[\s]?(.*)",markdown):
        return BlockType.QUOTE

    # - 
    if re.findall(r"- (.*)",markdown):
        return BlockType.ULIST

    # 1.
    if re.findall(r"\d. (.*)",markdown): 
        return BlockType.OLIST

    else:
        return BlockType.PARA








