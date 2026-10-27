import unittest
from extract import extract_markdown_images, extract_markdown_links
from split import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

class TestExtract(unittest.TestCase): 


    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another bit of text with an ![image2](secondurl) and a [link](linkurl)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"),("image2","secondurl")], matches)




    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another bit of text with an [link1](link1url) and a [link2](link2url)"    )
        self.assertListEqual([("link1", "link1url"),("link2","link2url")], matches)


if __name__ == "__main__": 
    unittest.main()
