from textnode import TextNode 
from textnode import TextType

def main(): 
    dummy = TextNode('this is some anchor text',TextType.LINK,'https://www.boot.dev')
    print(dummy) 

    # hello world
    print('hello world')

main()
