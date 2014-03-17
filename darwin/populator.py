import random
import requests
from deap import gp,tools
from helper import *
import pygraphviz as pgv
import time

__author__ = 'MrJew'

class Populator:
    configuration = None
    population = None
    toolbox = None
    hof = None
    parameters = None

    def __init__(self,configuration=None):
        if configuration!=None:
            self.configuration = configuration
            self.toolbox = configuration.toolbox
            self.population = self.toolbox.population(n=configuration.pop)
            self.parameters = self.collectFitnessFromTarget()
            self.hof = tools.HallOfFame(self.configuration.hofnum)


    def nonEvaluated(self,offspring):
        """ Crete a list of all nonevaluated individuals in the population """
        return [ind for ind in offspring if not ind.fitness.valid]

    def generateSource(self,individual):
        """Takes all the information from the configuration file and represents the source of the individual """
        source = self.configuration.configClass.getSource(self.configuration.imports,
                                                          self.lambdify(gp.stringify(individual),self.configuration.pset),
                                                          getSignature(self.configuration.testArguments))
        return source

    def evaluate(self,individual):
        """ Prepares the paramters and sends a request towards the evaluating
            web service and returns the fitness for the called individual"""


        print individual
        destination = "/evaluate"

        args={"individual"  : self.generateSource(individual),
              "arguments"   : self.parameters,
              }

        try:
            r = requests.get(self.configuration.evalUrl+destination,params=args)
            result = float(r.text)

        except:
            e = sys.exc_info()[0]
            print e
            result = 500.0



        print result
        return result,

    def lambdify(self,expr, pset):
        """ given an individual and a pset it evaluates the individual and returns it back as a callable instance """
        args = ",".join(arg for arg in pset.arguments)
        lstr = "lambda {args}: {code}".format(args=args, code=expr)
        return lstr

    def collectFitnessFromTarget(self):
        """ When cloning a service it's used for generating list of fitness based
            on the results from the web service """
        kwargs = listTokwags(self.configuration.testArguments)
        fitnessList = []
        if self.configuration.copyUrl:
            for kwarg in kwargs:
                r = self.configuration.configClass.requestHandler(self.configuration.copyUrl,kwarg)
                fitnessList.append([kwarg,r])
        else:
            for kwarg in kwargs:
                r = self.configuration.getFitnessFunction()(**kwarg)
                fitnessList.append([kwarg,float(r)])

        return str(fitnessList)

    def crossover(self):
        """ Given a generation it mates all the individuals based on the crossover parameter"""
        for i in range(1, len(self.offspring), 2):
            if random.random() < self.configuration.cx:
                self.offspring[i-1], self.offspring[i] = self.toolbox.mate(self.offspring[i-1], self.offspring[i])
                del self.offspring[i-1].fitness.values, self.offspring[i].fitness.values

    def mutation(self):
        """ Given a generation it mutates the individuals based on the mutation parameter"""
        for i in range(len(self.offspring)):
            if random.random() < self.configuration.mut:
                self.offspring[i], = self.toolbox.mutate(self.offspring[i])
                del self.offspring[i].fitness.values

    def populate(self):
        """ Generates all the populations that are evaluated, mutated, mated and when
            all the generations finish it returns a list of the top 20 individuals"""

        for gen in range(self.configuration.gen):

            self.offspring = self.toolbox.select(self.population, len(self.population))
            self.offspring = map(self.toolbox.clone, self.offspring)
            self.crossover()
            self.mutation()
            invalid_ind = self.nonEvaluated(self.offspring)
            fitnesses = self.toolbox.map(self.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            self.population = self.offspring
            self.hof.update(self.population)
            if self.hof[0].fitness.values[0]==0.0:
                break

        self.outputIndividuals()

    def outputIndividuals(self):
        inds = []
        for ind in self.hof:
             inds.append((gp.stringify(ind), ind.fitness))
        return inds

    def generateWebService(self,individual):
        generateService(self.configuration.imports,
                        getSignature(self.configuration.testArguments),
                        self.lambdify(gp.stringify(individual),self.configuration.pset),
                        self.configuration.configClass,)

    def draw(self,expr,fname):
        nodes, edges, labels = gp.graph(expr)
        g = pgv.AGraph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog="dot")

        for i in nodes:
            n = g.get_node(i)
            n.attr["label"] = labels[i]

        g.draw(fname)