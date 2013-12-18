__author__ = 'MrJew'

import inspect
import sys

class BaseConfig:

    def getFunctions(self):
        """ returns a list of all the non predefined functions in the extended class """
        listOfMethods = dir(self)
        listOfExcludes = ["functionArgs","fitnessFunction","numberOfFunctionArgs","getFunctions","__doc__","__module__","__init__"]
        listOfMethods = [(getattr(self,method), self.numberOfFunctionArgs(method)) for method in listOfMethods if method not in listOfExcludes ]
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