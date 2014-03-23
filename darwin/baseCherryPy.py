__author__ = 'MrJew'

import sys
from helper import stdoutIO

class BaseCherryPy:

    def evaluate(self,individual,arguments):
        """ Evaluate method that acts as a fitness function for the darwin framework used by the evaluator"""
        arguments = eval(arguments)
        diff=0
        for i in arguments:
            sys.argv = i[0]
            with stdoutIO() as s:
                exec(individual) in {}
            try:
                res = float(s.getvalue())
                diff += (res - i[1])**2
            except:

                diff = sys.float_info.max

        return str(diff)

    evaluate.exposed=True






