__author__ = 'MrJew'


from baseConfig import BaseConfig
from runner import runGP

class Config(BaseConfig):

    def mul(self,a,b):
        return operator.mul(a,b)

    def add(self,a,b):
        return operator.add(a,b)

    def saveDiv(self,a,b):
        if b==0:
            return 0
        else:
            return a/b

    def subtract(self,a,b):
        return operator.sub(a,b)


#c = Configuration(configClass=Config(),pop=1000,gen=100,cx=0.9,mut=0.1,maxDepthLimit=10,
#                  evaluatingService="http://localhost:8844",
#                  copyService="http://localhost:8080",testArguments=arguments,imports=imports)


