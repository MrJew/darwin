__author__ = 'MrJew'
from helper import *
import inspect
import sys
import operator
import math
import requests



class Handlers:

    def handler(self,url,params=None):
        if params:
            r = requests.get(url,params=params)
        else:
            r = requests.get(url)
        print r.text
        return self.responseHandler(r)

    def requestHandler(self,url,params):

        return self.handler(url,params)


    def responseHandler(self,r):
        return float(r.text)


class PrimitiveConfig(Handlers):
    listOfExcludes = ["listOfExcludes","getSource","getPrimitives","functionArgs","updateExcludes",
                      "fitnessFunction","numberOfFunctionArgs","getFunctions","basicPrimitives"
                      ,"requestHandler","responseHandler", "handler",
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
        try:
            return math.sin(a)
        except:
            return 0

    def cos(self,a):
        try:
            return math.cos(a)
        except:
            return 0

    def sqrt(self,a):
        if a>0:
            return math.sqrt(a)
        else:
            return 0

    def pow(self,a,b):
        try:
            return math.pow(a,b)
        except:
            return 0

    def log(self,a):
        try:
            return math.log(a)
        except:
            return 0

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
        result = generateImports(imports)
        result+= generateFunctions(self,False)
        result += generateMain(arguments,individual,False)
        result += "print main(**sys.argv)\n"
        return result



