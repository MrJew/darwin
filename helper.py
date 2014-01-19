__author__ = 'MrJew'
import sys
import StringIO
import contextlib

def listTokwags(dicOfLists):
    newArgs=[]
    for i in range(len(dicOfLists.values()[0])):
        nd={}
        for key in dicOfLists.keys():
            nd[key]=dicOfLists[key][i]
        newArgs.append(nd)
    return newArgs

def formatCode(method):
    method = method.split('\n')
    newList = []
    for line in method:
        newList.append(line[4:])

    result = ""
    for line in newList:
        result += line+"\n"

    return result[:-1]

def getSignature(arguments):
    """takes dictionary and creates a function signature based on the keys"""
    result=""
    for arg in arguments.keys():
        result+=arg+","
    return result[:-1]

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