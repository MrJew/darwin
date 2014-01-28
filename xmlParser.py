__author__ = 'mrjew'
from lxml import etree

# create XML
def generateXML(fname=None,arguments=None,primitives=None,terminals=None,customPrimitives=None,
                pop=None,gen=None,cx=None,mut=None,evalUrl=None,copyUrl=None,imports=None):

    children={}
    if pop : children['pop']=pop
    if gen : children['gen']=gen
    if cx  : children['cx']=cx
    if mut : children['mut']=mut
    if arguments  : children['args']=str(arguments)
    if terminals  : children['terminals']=str(terminals)
    if primitives : children['basicPrimitives']=str(primitives)
    else: children['basicPrimitives']=str([])
    if customPrimitives : children['customPrimitives']=str(customPrimitives)
    else: children['customPrimitives']=str([])
    if evalUrl    : children['evalUrl']=evalUrl
    if copyUrl    : children['copyUrl']=copyUrl

    root = etree.Element('config')

    # another child with text
    for value in children.keys():
        child = etree.Element(value)
        child.text = children[value]
        root.append(child)

    s = etree.tostring(root, pretty_print=True)

    f = open(fname,"w")
    f.write(s)
    f.close()


arguments = {'x':[1,2,3,4],'y':[1,2,3,4],'z':[1,2,3,4]}
primitives = ["add","mul","safeDiv","sub"]
terminals = [1]

generateXML(fname="./sample/config.xml",arguments=arguments,primitives=primitives,terminals=terminals,
            pop='1000',gen='1000',cx='0.8',mut='0.2',evalUrl="http://localhost:8844",copyUrl="http://localhost:8080")