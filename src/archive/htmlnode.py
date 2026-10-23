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
