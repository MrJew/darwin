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
    if arguments  : children['args']=arguments
    if terminals  : children['terminals']=terminals
    if primitives : children['basicPrimitives']=primitives
    else: children['basicPrimitives']=[]
    if customPrimitives : children['customPrimitives']=customPrimitives
    else: children['customPrimitives']=[]
    if evalUrl    : children['evalUrl']=evalUrl
    if copyUrl    : children['copyUrl']=copyUrl
    if imports    : children['imports']=imports
    else: children['imports']=[]
    root = etree.Element('config')

    # another child with text
    for value in children.keys():
        if value == 'args':
            args = etree.Element("arguments")
            for argname in children['args'].keys():
                for i in range(len(children['args'][argname])):
                    arg = etree.Element("arg",name=str(argname),number=str(i))
                    arg.text=str(children['args'][argname][i])
                    args.append(arg)
            root.append(args)
        elif value == 'terminals':
            terms = etree.Element("terminals")
            for t in children["terminals"]:
                term = etree.Element("terminal")
                term.text = str(t)
                terms.append(term)
            if len(children["terminals"])!=0 : root.append(terms)
        elif value == 'basicPrimitives':
            bprims = etree.Element("basicPrimitives")
            for primitive in children["basicPrimitives"]:
                prim = etree.Element("primitive")
                prim.text=primitive
                bprims.append(prim)
            if len(children["basicPrimitives"])!=0 : root.append(bprims)
        elif value == 'customPrimitives':
            cprims = etree.Element("customPrimitives")
            for primitive in children["customPrimitives"]:
                prim = etree.Element("primitive")
                prim.text=primitive
                cprims.append(prim)
            if len(children["customPrimitives"])!=0: root.append(cprims)
        elif value == "imports":
            imps = etree.Element("imports")
            for imp in children["imports"]:
                port = etree.Element("import")
                port.text = imp
                imps.append(port)
            if len(children["imports"])!=0 : root.append(imps)
        else:
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


tree = etree.parse("./sample/config.xml")
root = tree.getroot()
terminals = []
arguments = {}
imports = []
primitives = []
customPrimitives=[]
for child in root:
    if child.tag == "terminals":
        terms = root.find(child.tag)
        for t in terms:
            terminals.append(float(terms.find(t.tag).text))
        print terminals
    elif child.tag == "imports":
        imps = root.find(child.tag)
        for i in imps:
            imports.append(i.text)
        print imports
    elif child.tag == "basicPrimitives":
        imps = root.find(child.tag)
        for i in imps:
            primitives.append(i.text)
        print primitives
    elif child.tag == "customPrimitives":
        imps = root.find(child.tag)
        for i in imps:
            customPrimitives.append(i.text)
        print customPrimitives
    elif child.tag == "arguments":
        args = root.find(child.tag)
        for a in args:
            if a.get("name") not in arguments:
                arguments[a.get("name")]=[]
            arguments[a.get("name")].append(float(a.text))
        print arguments

    else:
        print child.tag,root.find(child.tag).text