import unittest
import everything
from everything import TextNode
from everything import TextType
from everything import text_node_to_html_node
from everything import BlockType
from everything import block_to_block_type
from everything import split_nodes_delimiter
from everything import split_nodes_image, split_nodes_link
from everything import text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self): 
        node = TextNode("This is a text node", TextType.BOLD) 
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url(self): 
        node = TextNode("This is a text node", TextType.LINK,'http://www.boot.dev')
        self.assertNotEqual(node.url, None)


    def test_text_type(self): 
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_delim(self): 
        string_list = [TextNode('This is a test with a **bolded phrase** in the middle',TextType.TEXT), TextNode('and another **bold** test',TextType.TEXT)]
        split = split_nodes_delimiter(string_list, '**', TextType.BOLD)
        expected = [TextNode("This is a test with a ", TextType.TEXT),TextNode("bolded phrase", TextType.BOLD),TextNode(" in the middle", TextType.TEXT),TextNode("and another ",TextType.TEXT), TextNode("bold",TextType.BOLD),TextNode(" test",TextType.TEXT,)]
        self.assertEqual(split,expected)


    def test_split_images(self):
        
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",TextType.TEXT, )
        
        new_nodes = split_nodes_image([node])
        
        comparison =  [TextNode("This is text with an ", TextType.TEXT),TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),TextNode(" and another ", TextType.TEXT),TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),]
        
        print(f'\n new nodes = {new_nodes}\n') 
        
        print(f'comparison = {comparison}')


        self.assertListEqual(new_nodes,comparison)

    def test_split_links(self):
       
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        
        new_nodes = split_nodes_link([node])
        
        comparison =   [TextNode("This is text with a link ", TextType.TEXT),TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),]

        print(f'\n new nodes = {new_nodes}\n') 
        
        print(f'comparison = {comparison}')


        self.assertListEqual(new_nodes,comparison)


    def test_text_to_nodes(self): 
        
        input_text = f'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        
        output = text_to_textnodes(input_text)

        expected = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        
        self.assertEqual(output,expected)


    def test_blocktypes(self): 
        heading = '### This is a heading'
        code_block = '```\nThis is code```'
        quote_block = '> This is a quote'
        UL_block = '- This is\n- an unordered\n-list'
        OL_block = '1. This is\n2. an unordered\n one'
        parablock = 'and this is just a regular\nparagraph\nyadig?'

        self.assertEqual(BlockType.HEAD,block_to_block_type(heading)) 
        self.assertEqual(BlockType.PARA,block_to_block_type(parablock)) 
        self.assertEqual(BlockType.CODE,block_to_block_type(code_block))  
        self.assertEqual(BlockType.QUOTE,block_to_block_type(quote_block)) 
        self.assertEqual(BlockType.ULIST,block_to_block_type(UL_block)) 
        self.assertEqual(BlockType.OLIST,block_to_block_type(OL_block)) 



        












if __name__ == "__main__":
    unittest.main()
