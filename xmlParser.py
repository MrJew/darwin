__author__ = 'mrjew'
from lxml import etree


arguments = {'x':[1,2,3,4],'y':[1,2,3,4],'z':[1,2,3,4]}
primitives = ["add","mul","safeDiv","sub"]
terminals = [1]
customPrimitives = []

children = {"pop":'1000',"gen":'1000',"cx":'0.8',"mut":'0.2',"evalUrl":"http://localhost:8844",
            "copyUrl":"http://localhost:8080","import":"operator","args":str(arguments),
            "basicPrimitives":str(primitives),"terminals": str(terminals),"customPrimitives":str(customPrimitives)}

# create XML
root = etree.Element('config')

# another child with text
for value in children.keys():
    child = etree.Element(value)
    child.text = children[value]
    root.append(child)

s = etree.tostring(root, pretty_print=True)

f = open("config.xml","w")
f.write(s)
f.close()

tree = etree.parse("testConfig.xml")
root = tree.getroot()
children = []
for child in root:
    children.append(child.tag)

for child in children:
    print child,root.find(child).text