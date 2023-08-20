#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse, random, importlib
sys.path.insert(0, "Scripts")
sys.path.insert(0, "Libs")

###############################################
##### Entry point:        #####################
###############################################
def Main():
    # See: https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Build Bot entry point.')
    
    #######################################################
    ##### Configuring the syntax of the cmdline:    #######
    #######################################################
    # Positionl arguments are defined this way:
    parser.add_argument('scriptname',           help='The name of the package to build, or "all" to build every package.',
        type=str)
    
    #parser.add_argument('--service',            help='Meant to run Odoo as a service. No privilege setup is made.',
    #    action='store_const', const=True, default=False)
    
    # Parsing proper:
    args = parser.parse_args()
    #print(args) ; return
    
    #################################################
    ##### Semantic checks:        ###################
    #################################################
    if not args.scriptname:
        print("A scriptname argument is mandatory.")
        exit(-1)
    
    #######################################################
    ##### Do the payload itself:        ###################
    #######################################################
    # Load and import the requested script:
    scriptname = args.scriptname
    print("Loading DEB-building script: %s" % scriptname)
    script_module = importlib.import_module(scriptname)
    
    #import python_38_complete
    #python_38_complete.Prepare1("batatas")

if __name__ == "__main__": Main()