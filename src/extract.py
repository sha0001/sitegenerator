import re

# images ![stuff](stuff) 
def extract_markdown_images(text): 
    return re.findall(r"\!\[(.*?)\]\((.*?)(?=\))",text) 

# links 
def extract_markdown_links(text): 
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)(?=\))",text)

