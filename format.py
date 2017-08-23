import xml.etree.cElementTree as ET
import json

input_file = "patents.json"

with open(input_file, 'r') as f:
	data = json.load(f)

root = ET.Element("searchresult")
ET.SubElement(root, "query").text = "Denso Corporation"

for i in range(len(data)):
	doc = ET.SubElement(root, "document", id=str(i))
	ET.SubElement(doc, "title").text = data[i]["title"]
	ET.SubElement(doc, "url").text = data[i]["url"]
	ET.SubElement(doc, "snippet").text = data[i]["snippet"]

tree = ET.ElementTree(root)
tree.write("patents.xml")