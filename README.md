Darwin
=================================================================================================
                                                                                
                                                                       . :.           MMMO          
                                                                .M,    MMMM.         .MMMM          
                                                                   .M OMMMM.         MMMMN          
                                                       .NMMN,         MMMN         .MMMM            
                                            :MM:       MMMMM.        MMMM :MN.     .MMMMM           
                                            MMMM.     MMMMM          MMMMMN N,M    .MMMMM.          
                                         ,MMM:,      .MMMMM          MMMMMMM.      MMMMMM,          
                                         MMMMN.       MMMMM         .MMMMMMN       MMMMMMMMMN,      
                                        DMMMMM.      MMMMMM         .MMMMM..       MMMMMM    M      
                                MMMM,  OMMMMMMMM,     MMMM:M.       NMMMMM.        MMMMM.           
                            .MMMMMMMM  MMMMMM   DM.  MMMMM .M.      .MMMMM        .MMMMMM.          
                           NMMMMMM      MMMM,   .N   ~MMM.  .M       :MMMM.        MMMNMMM.         
                         ,MMMMMMM.     :MMMMM?.       MMMM .MN       MMMMM:        ,MM  MMM         
                        OMMMMMMMM       NMM.MMM.     ,MMMMM          NMMNMM        MMD   MMM        
                        MMMMMMMMMM       MM .MMM     NMN .MD        MMM ~MM.      MMM.   .MM.       
                          MMMMM,NM       NM  MM.    MMM   MM.      MM, .MMM     .MM       MMM       
                        :MMMOMM..M.  ~MMMMN. MM.  .MM,    MM.    MM..   .MM     ,M        .MM.      
                      ,MMD,  MM  .N  MN      MM   .M.     ,M.   ,MM      MM     M8          MMMNM   
                      ~M.   .MMM.ND  MM.     MMMM  MM.     MMMM. .MM     NMMNM. ,MMD,       ,M..    
 

Basic Example
=================================================================================================
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

    class Config(PrimitiveConfig):

        def fitnessFunction(self,x,y,z):
            return x + y + z/3

    runGP(configClass=Config(),xmlConfig="config.xml")

Where "config.xml" is the location of the configuration XML you want to use


Advanced Example
=================================================================================================
Custom Primitives:
In more advance cases you would want to configure the framework ourselves. You might want to activate
special features or set certain parameters. For example primitive sets might not be good enough
and you need additional one. What you need to do is simply extend PrimitiveConfig.

For example:

    class Config(PrimitiveConfig):
    
        def myComplextMath(self,x,y,z):
            return x + y - z*2 - 1

        def specialMathFunction(self,a,b,c):
            return a*b*(c-1)
            
    runGP(configClass=Config(),xmlconfig="config.xml")
    
The way PrimitiveConfig works is except the methods [name of used methods] every other method name is
generating a primitive set the framework is using. 
=================================================================================================
Tests
===============================================================================================

