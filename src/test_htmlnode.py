import unittest
from htmlnode import HTMLnode 
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLnode(unittest.TestCase):


    def test_props(self):
        node = HTMLnode("tag","value",["child1","child2","child3"],{"href": "https://www.google.com","target": "_blank"})
        expected = f'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(),expected)

    def test_to_html(self): 
        node = HTMLnode("tag","value",["child1","child2","child3"],{"href": "https://www.google.com","target": "_blank"})
        try: 
            node.to_html()
        except NotImplementedError: 
            print('NotImplementedError working as expected')

    def test_tag(self): 
        node = HTMLnode("tag","value",["child1","child2","child3"],{"href": "https://www.google.com","target": "_blank"})
        expected = "tag"

        self.assertEqual(node.tag,expected)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__": 
    unittest.main()
    
