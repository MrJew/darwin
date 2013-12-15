import os.path
import ast

class FunctionIOCatcher:
    filePath = None
    inputArgs = None
    outputArgs = None
    funcName = None

    """ Creates a class to which you give input/output arguments of your function so
    	they can be stored for later use """

    def __init__(self,path,functionName):
        self.filePath = path;
        self.funcName = functionName

        if not os.path.exists(self.filePath):
            f = open(self.filePath,'w')
            f.close()

    def catchInput(self,input):
        self.inputArgs = str(input)
        self.writeToFile(self.funcName+" "+self.inputArgs)

    def catchOutput(self,output):
        self.outputArgs = str(output)
        self.writeToFile(self.outputArgs)

    def writeToFile(self,arg):
        f = open(self.filePath,"a")
        f.write(arg+'\n')
        f.close()

class FunctionEvaluator:
    filePath = None
    lines = None
    functionCall = []
    settedClass = None

    def __init__ (self,path,setClass):
        self.filePath = path
        self.settedClass = setClass
        self.readLog()


    def readLog(self):
        f = open(self.filePath,"r")
        self.lines = f.readlines()
        f.close()
        counter = 1;
        while counter<len(self.lines):
            line = self.lines[counter-1].split(" ",1)
            fname = line[0]
            args = ast.literal_eval(line[1])

            self.functionCall.append({"fname":fname,"args":args,"return":self.lines[counter].rstrip()})
            counter+=2

    def evaluate(self):
        classMethods = dir(self.settedClass)
        result=[]
        for i in self.functionCall:
            if i['fname'] in classMethods:
                print i['return']
                print getattr(self.settedClass,i['fname'])(**i['args'])
                if i['return'] == getattr(self.settedClass,i['fname'])(**i['args']):
                    result.append(['True',i])
                else:
                    result.append(['False',i])
        return result