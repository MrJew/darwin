darwin
======

In the /sample folder are located the examples for the Client, evalator and the cloning instance. 

If you want to try the cloning example:

1. Run the Evaluator - cherrypyinstance.py
2. Run the service we are clonning - dummyinstance.py 
3. Run the Client - rungp.py *needs to be ran last*.

If you want to run only the evaluator and use your own fitness function

1. In rungp.py import baseConfig
2. create a class that extends BaseConfig
3. write a method with the name "fitnessFunction(self, args...) and give it a return statement
4. call runGP parsing as parameter the newly created config class

For example:

    class Config(BaseConfig):

        def fitnessFunction(self,x,y,z):
            return x + y + z/3

    runGP(configClass=Config(),xmlConfig="config.xml")

Where "config.xml" is the location of the configuration XML you want to use


