__author__ = 'mrjew'
from lxml import etree


def generateXML(fname=None,arguments=None,primitives=None,terminals=None,customPrimitives=None,
                pop=None,gen=None,cx=None,mut=None,evalUrl=None,copyUrl=None,imports=None):
    """Creates an xml file
        fname: file name of the xmlFile
        arguments: location of the .csv file contain the test arguments (e.g. /root/home/darwinProject/args.csb
        primitives: list of primitive names from the pre-set darwin primitives
        terminals: list of numbers
        customPrimitives: list of primitive names created by the user
        pop: number specifying the population size
        gen: number of generations
        cx: float number between 0.0-1.0 that specifies the crossing rate applied to the population
        mut:float number between 0.0-1.0 that specifies the mutation rate applied to the population
        evalUrl: full URL name to the target web service for evaluation
        copyUrl: full URL name to the target web service for cloning
        imports: list of names of modules used in the custom primitives """
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

def readXML(xmlFile):
    """ Given a location of an XML configuration file and returns a dictionary of it's data"""
    tree = etree.parse(xmlFile)
    root = tree.getroot()
    params = {}
    terminals=[]
    imports=[]
    primitives =[]
    customPrimitives=[]
    arguments={}


    for child in root:
        if child.tag == "terminals":
            terms = root.find(child.tag)
            for t in terms:
                terminals.append(float(terms.find(t.tag).text))
            params["terminals"]=terminals
        elif child.tag == "imports":
            imps = root.find(child.tag)
            for i in imps:
                imports.append(i.text)
            params["imports"]=imports
        elif child.tag == "basicPrimitives":
            imps = root.find(child.tag)
            for i in imps:
                primitives.append(i.text)
            params["basicPrimitives"]=primitives
        elif child.tag == "customPrimitives":
            imps = root.find(child.tag)
            for i in imps:
                customPrimitives.append(i.text)
            params["customPrimitives"]=customPrimitives
        elif child.tag == "arguments":
            args = root.find(child.tag)
            for a in args:
                if a.get("name") not in arguments:
                    arguments[a.get("name")]=[]
                arguments[a.get("name")].append(float(a.text))
            params["args"]=arguments
        else:
            params[child.tag]=child.text

    return params
