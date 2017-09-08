from xml.dom import minidom
import json

input_file = 'denso-corporation.xml'
output_file = 'patents_sub.json'
patent_file = 'patents.json'
xmldoc = minidom.parse(input_file)

clust = xmldoc.getElementsByTagName('group')
detect_clust = clust[2]

detect_doc = detect_clust.getElementsByTagName('document')
detect_doc_id = []
for doc in detect_doc:
	detect_doc_id.append(int(doc.attributes['refid'].value))

with open(patent_file) as f:
	patents = json.load(f)
patents_sub = [patents[i] for i in detect_doc_id]

with open(output_file, 'w') as f:
	f.write(json.dumps(patents_sub))