__author__ = 'MrJew'
from helper import *
import inspect
import sys
import operator
import math

class PrimitiveConfig:
    listOfExcludes = ["listOfExcludes","getSource","getPrimitives","functionArgs","updateExcludes",
                      "fitnessFunction","numberOfFunctionArgs","getFunctions","basicPrimitives",
                      "__doc__","__module__","__init__"]
    basicPrimitives = ["add","mul","sub","safeDiv","sin","cos","sqrt","pow","log"]

    def add(self,a,b):
        return operator.add(a,b)

    def mul(self,a,b):
        return operator.mul(a,b)

    def sub(self,a,b):
        return operator.sub(a,b)

    def safeDiv(self,a,b):
        if b==0:
            return 0
        else:
            return operator.div(a,b)

    def sin(self,a):
        return math.sin(a)

    def cos(self,a):
        return math.cos(a)

    def sqrt(self,a):
        if a>0:
            return math.sqrt(a)
        else:
            return 0

    def pow(self,a,b):
        return math.pow(a,b)

    def log(self,a):
        return math.log(a)

    def updateExcludes(self,chosenPrimitives):
        self.listOfExcludes.extend([ p for p in self.basicPrimitives if p not in chosenPrimitives ])

    def getPrimitives(self):
        return [method for method in dir(self) if method not in self.listOfExcludes]

    def getFunctions(self):
        """ returns a list of all the non predefined functions in the extended class """
        listOfMethods = dir(self)
        listOfMethods = [(getattr(self,method), self.numberOfFunctionArgs(method)) for method in listOfMethods if method not in self.listOfExcludes ]
        return listOfMethods

    def numberOfFunctionArgs(self,funcName):
        """ finds the number of arguments of a function from the extended class """
        func = getattr(self,funcName)
        return len(inspect.getargspec(func)[0])-1

    def functionArgs(self,funcName):
        """ finds the arguments of a function from the extended class """
        func = getattr(self,funcName)
        args = inspect.getargspec(func)[0]
        del args[0] # removes 'self'
        return args

    def getSource(self, imports,individual,arguments):
        result=""
        result+="import sys\n"
        result+="import operator\n"
        result+="import math\n"
        for i in imports:
            result +="import "+i+"\n"
        result+="\n"

        # getting the source and removing the self arg
        for method in self.getPrimitives():

            code = formatCode(inspect.getsource(getattr(self,method)))
            code = code.split("\n")
            args=''
            for arg in self.functionArgs(method):
                args=args+arg+','
            args=args[:-1]
            code[0] = "def "+method+"("+args+"):"

            for line in code:
                result += line +"\n"

        #add lambda
        main = "def main("+arguments+"):\n"
        for x in arguments.split(','):
            main += "    "+x+" = "+"float("+x+")\n"

        main +="    ind = "+individual+"\n"
        main +="    return ind("+arguments+")\n\n"
        main += "print main(**sys.argv)\n"

        result += main
        return result