__author__ = 'MrJew'

import inspect
import sys

class BaseConfig:

    def getFunctions(self):
        listOfMethods = dir(self)
        listOfExcludes = ["getImports","functionsToSouurce","fitnessFunction","numberOfFunctionArgs","getFunctions","__doc__","__module__","__init__"]
        listOfMethods = [(getattr(self,method), self.numberOfFunctionArgs(method)) for method in listOfMethods if method not in listOfExcludes ]
        return listOfMethods

    def numberOfFunctionArgs(self,funcName):
        func = getattr(self,funcName)
        return len(inspect.getargspec(func)[0])-1
