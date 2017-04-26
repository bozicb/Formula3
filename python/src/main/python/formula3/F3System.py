import formula3.utils.SLF4J2PyLogging as javalogging

logger=javalogging.getLogger("F3System")

import sys
import pkgutil

import globals

import os.path

def addF3Operator(name, opCode):
    ' Add an operator of given name to F3.'
    # Note that the current scheme of storing (a simple dict) 
    # will overwrite a routine that has already been added.
    # Later versions should change that (think operator overloading
    # and semantic aware selection of operators)
    
    #other ideas: Is it possible to check operator parameters to find bogus operators before the act?
    globals.aggregates[name] = opCode               # Very simple approach right now :-) 
    
    

def addF3PackagePath(path):
    
    # What this routine shall do: 
    # Look into the given path
    # walk all directories and load the package
    # Note, that this will load the __init__.py of the module which in turn must 
    # actively register the F3 extensions
    
    logger.info("Adding path "+str(path))
    
    absPath=os.path.abspath(path)   # Mainly to make debugging/troubleshooting more convenient. 
                                    # This way we make it clear what's going on even when the path given is relative
    logger.info("This is an absPath of "+str(absPath))
    
    for importer, name, ispkg in pkgutil.iter_modules([absPath], ''):
        logger.info("Inspecting "+name+" with package status "+str(ispkg)+" from "+importer.path)
        if ispkg:
            impLoader=importer.find_module(name)
            impLoader.load_module(name)
    
def getOperatorList():
    return globals.aggregates.keys()
