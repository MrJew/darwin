import random
import requests
from deap import gp,tools
from helper import *


__author__ = 'MrJew'

class Populator:
    configuration = None
    population = None
    toolbox = None
    topTwenty = []
    hof = tools.HallOfFame(1)
    parameters = None

    def __init__(self,configuration):
        self.configuration = configuration
        self.toolbox = configuration.toolbox
        self.population = self.toolbox.population(n=configuration.pop)
        self.parameters = self.collectFitnessFromTarget()


    def crossover(self,offspring):
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.configuration.cx:
                self.toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

    def mutation(self,offspring):
        for mutant in offspring:
            if random.random() < self.configuration.mut:
                self.toolbox.mutate(mutant)
                del mutant.fitness.values

    def nonEvaluated(self,offspring):
        return [ind for ind in offspring if not ind.fitness.valid]

    def evaluate(self,individual):
        parameters = str(self.configuration.testArguments)

        destination = "/evaluate"
        if self.configuration.copyService:
            destination = "/evaluateCopy"
        args={"individual"  : gp.stringify(individual),
              "arguments"   : self.parameters,
              "logfile"     : "log.txt"}
        r = requests.get(self.configuration.cloud+destination,params=args)
        result = float(r.text)
        print result
        if result == 0.0: self.topTwenty.append(individual)
        return result,

    def collectFitnessFromTarget(self):
        kwargs = listTokwags(self.configuration.testArguments)
        fitnessList = []
        for kwarg in kwargs:
            r = requests.get(self.configuration.copyService,params=kwarg)
            fitnessList.append([kwarg,float(r.text)])
        return str(fitnessList)

    def populate(self):
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
            if len(self.topTwenty)>=20:
                break

        print gp.stringify(self.hof[0])
        print self.hof[0].fitness