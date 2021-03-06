__author__ = 'MrJew'
import sys
import StringIO
import contextlib
import inspect

def listTokwags(dicOfLists):
    """ based on a dictionary that contains an argument name and list of arguments as a value it creates
        a list of dictionaries used as kwargs"""
    newArgs=[]
    for i in range(len(dicOfLists.values()[0])):
        nd={}
        for key in dicOfLists.keys():
            nd[key]=dicOfLists[key][i]
        newArgs.append(nd)
    return newArgs

def formatCode(method):
    """ formats the method by removing the 'self' parameter"""
    method = method.split('\n')
    newList = []
    for line in method:
        newList.append(line[4:])

    result = ""
    for line in newList:
        result += line+"\n"

    return result[:-1]

def formatLines(code):
    """formats the code by tabbing it correctly"""
    lines = code.split('\n')
    formated = []
    for line in lines:
        if line!='':
            formated.append("    "+line)
        else:
            formated.append(line)
    result = '\n'.join(formated)
    return result

def getSignature(arguments):
    """takes dictionary and creates a function signature based on the keys"""
    result=""
    for arg in arguments.keys():
        result+=arg+","
    return result[:-1]

def individualForMethods(individual,config):
    """ Creates an individual for a lambda expression by adding self notation so they can be executed in a class"""
    f = dir(config)
    for i in f:
        old = i+"("
        new = "self."+i+"("
        individual=individual.replace(old,new)
    return individual

def generateService(imports,arguments,individual,config):
    """ Generates a cloned webservice using a standard individual and adding CherryPy wrapper
        imports: list of imports used by the custom primitves
        individual: DEAP individual
        arguments: dictionary arguments
        config: configuration class used in the framework
     """
    result = "from baseCherryPy import BaseCherryPy\n"
    if len(imports)==0:
        imports = ['cherrypy']
    else:
        imports.append('cherrypy')
    result += generateImports(imports)

    result += "########################### CONFIG ##############################\n"
    result += "cherrypy.config.update({'server.socket_host': '',	\n"
    result += "                    'server.socket_port': 8844,})				\n"
    result += "#################################################################\n\n"
    result += "class ClonedWebService(BaseCherryPy):\n\n"
    result += formatLines(generateFunctions(config,True))
    result += formatLines(generateMain(arguments,individualForMethods(individual,config),True))
    result += "    def index(self,"+arguments+"):\n"
    result += "        return self.main("+arguments+")\n"
    result += "    index.exposed = True\n\n"
    result += "cherrypy.quickstart(ClonedWebService())"
    f = open("clonedwebservice.py","w")
    f.write(result)
    return result


def generateImports(imports):
    """ Generate lines that specify imports used by the individual """
    result=""
    result+="import sys\n"
    result+="import operator\n"
    result+="import math\n"
    for i in imports:
        result +="import "+i+"\n"
    result+="\n"
    return result

def generateFunctions(config,service):
    """ based on the primitives extracts the function code and formats it correctly """
    result = ''
    for method in config.getPrimitives():

        code = formatCode(inspect.getsource(getattr(config,method)))
        code = code.split("\n")
        args=''
        for arg in config.functionArgs(method):
            args=args+arg+','
        args=args[:-1]
        if not service:
            code[0] = "def "+method+"("+args+"):"
        else:
            code[0] = "def "+method+"(self,"+args+"):"


        for line in code:
            result += line +"\n"
    return result

def generateMain(arguments,individual,service):
    """ creates a main function in the individual called by the evaluator to get the individual result """
    if not service:
        main = "def main("+arguments+"):\n"
    else:
        main = "def main(self,"+arguments+"):\n"
    for x in arguments.split(','):
        main += "    "+x+" = "+"float("+x+")\n"
    main +="    ind = "+individual+"\n"
    main +="    return ind("+arguments+")\n\n"

    return main


##############################################################################################################
## THE CODE BENEATH IS NOT MINE IT IS CREATED BY STACKOVERFLOW USER isedev AND THE CODE IS TAKEN            ##
## FROM THE THREAD http://stackoverflow.com/questions/14708216/showing-current-output-from-exec-in-python   ##
## ADDRESSING THE ISSUE OF REDIRECTING STANDARD OUTPUT IN A DIFFERENT CONTEXT BACK TO THE ORIGINAL ONE      ##
##############################################################################################################
class Proxy(object):

    def __init__(self,stdout,stringio):
        self._stdout = stdout
        self._stringio = stringio

    def __getattr__(self,name):
        if name in ('_stdout','_stringio','write'):
            object.__getattribute__(self,name)
        else:
            return getattr(self._stringio,name)

    def write(self,data):
         self._stdout.write(data)
         self._stringio.write(data)

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = Proxy(sys.stdout,stdout)
    yield sys.stdout
    sys.stdout = old