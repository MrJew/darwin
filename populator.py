import random
import requests
from deap import gp,tools
from helper import *


__author__ = 'MrJew'

class Populator:
    configuration = None
    population = None
    toolbox = None
    hof = None
    parameters = None

    def __init__(self,configuration):
        self.configuration = configuration
        self.toolbox = configuration.toolbox
        self.population = self.toolbox.population(n=configuration.pop)
        self.parameters = self.collectFitnessFromTarget()
        self.hof = tools.HallOfFame(self.configuration.hofnum)

    def crossover(self,offspring):
        """ Given a generation it mates all the individuals based on the crossover parameter"""
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.configuration.cx:
                self.toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

    def mutation(self,offspring):
        """ Given a generation it mutates the individuals based on the mutation parameter"""
        for mutant in offspring:
            if random.random() < self.configuration.mut:
                self.toolbox.mutate(mutant)
                del mutant.fitness.values

    def nonEvaluated(self,offspring):
        """ Crete a list of all nonevaluated individuals in the population """
        return [ind for ind in offspring if not ind.fitness.valid]

    def evaluate(self,individual):
        """ Prepares the paramters and sends a request towards the evaluating
            web service and returns the fitness for the called individual"""
        destination = "/evaluate"
        if self.configuration.copyService:
            destination = "/evaluateCopy"
        args={"individual"  : gp.stringify(individual),
              "arguments"   : self.parameters,
              "logfile"     : "log.txt",
              "logging"     : self.configuration.logging,
              "isMax"       : self.configuration.isMax}
        r = requests.get(self.configuration.cloud+destination,params=args)
        result = float(r.text)
        print result
        if result == 0.0: self.topTwenty.append(individual)
        return result,

    def collectFitnessFromTarget(self):
        """ When cloning a service it's used for generating list of fitness based
            on the results from the web service """
        kwargs = listTokwags(self.configuration.testArguments)
        fitnessList = []
        for kwarg in kwargs:
            r = requests.get(self.configuration.copyService,params=kwarg)
            fitnessList.append([kwarg,float(r.text)])
        return str(fitnessList)

    def populate(self):
        """ Generates all the populations that are evaluated, mutated, mated and when
            all the generations finish it returns a list of the top 20 individuals"""
        for gen in range(self.configuration.gen):
            offspring = self.toolbox.select(self.population, len(self.population))
            offspring = map(self.toolbox.clone, offspring)
            self.crossover(offspring)
            self.mutation(offspring)
            invalid_ind = self.nonEvaluated(offspring)
            fitnesses = self.toolbox.map(self.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            self.population = offspring
            self.hof.update(self.population)

        print gp.stringify(self.hof[0])
        print self.hof[0].fitness