__author__ = 'MrJew'

import cherrypy
from functionCatcher import FunctionIOCatcher
from helper import *

class BaseCherryPy:
    configuration = None
    _cp_config = {'tools.logger.on': True}

    def __init__(self,configuration):
        self.configuration = configuration

    def lambdify(self,expr, pset):
        """ given an individual and a pset it evaluates the individual and returns it back as a callable instance """
        print expr
        args = ",".join(arg for arg in pset.arguments)
        lstr = "lambda {args}: {code}".format(args=args, code=expr)
        return eval(lstr, dict(pset.context))

    def logger(self=None):

        """ handles the request after it goes into any cherrypy method, input/output logging is done here """
        if cherrypy.request.params['logging']:
            params = cherrypy.request.params['logfile']
            functionCatcher = FunctionIOCatcher(str(params),"evaluate")
            functionCatcher.catchInput(cherrypy.request.params)
            functionCatcher.catchOutput(cherrypy.response.body)

    def evaluate(self,individual,arguments,logging,logfile=None):
        """ Is called for individual evaluation not when copying
            *individual* : the individual that is being evaluated
            *arguments*  : arguments to test the individual with
            *logfile*    : name of the logfile used for the logger not gere
        """

        arguments = eval(arguments)
        newArgs = listTokwags(arguments)
        func = self.lambdify(individual,self.configuration.pset)
        fitness = self.configuration.getFitnessFunction()
        diff=0
        for i in newArgs:
            diff += (func(**i) - fitness(**i))**2
        return str(diff)

    evaluate.exposed=True

    def evaluateCopy(self,individual,arguments,logging,logfile=None):
        arguments = eval(arguments)
        func = self.lambdify(individual,self.configuration.pset)
        diff=0
        for i in arguments:
            diff += (func(**i[0]) - i[1])**2
        return str(diff)

    evaluateCopy.exposed=True

    cherrypy.tools.logger = cherrypy.Tool('before_finalize', logger)





