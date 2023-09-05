#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse, unittest
sys.path.insert(0, "Scripts")
sys.path.insert(0, "Libs")

###############################################
##### Operating modes:               ##########
###############################################
def op_run_lib_tests():
    # Run the tests as if invoked from the command line:
    unittest.main(module="deb_building_lib.testcases", argv=sys.argv[0:1], verbosity=2)

###############################################
##### Command line semantics:        ##########
###############################################
def get_cmdline_semantics(args, modes):
    # Get the line for the current mode, based on flags:
    matching_modes = []
    for mode in modes:
        # Any key in this mode exists in parsed args?
        this_mode_keywords = [
            modekey
            for modekey in mode[0]
            if getattr(args, modekey, False)
            ]
        # If at least one if the keys of this mode exists on parsed args:
        if len(this_mode_keywords) >= 1:
            matching_modes.append(mode)
    # Echo an error if the arguments match more than one mode:
    if len(matching_modes) == 0:
        print("Too few arguments.")
        exit(-1)
    if len(matching_modes) > 1:
        print("Arguments belonging to more than one operating mode: %s" % (
            ', '.join([ repr(mod[2]) for mod in matching_modes ]),
            ))
        exit(-1)
    return matching_modes

###############################################
##### Entry point:        #####################
###############################################
def Main():
    # See: https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser(description='Manage BuildBot-related unit tests.')
    
    #######################################################
    ##### Configuring the syntax of the cmdline:    #######
    #######################################################
    # Positional arguments are defined this way:
    #parser.add_argument('source_dir',                           help='Base directory for source',
    #    type=str)
    
    # Boolean flags:
    parser.add_argument('--run-lib-tests',                help='Run install engine tests.',
        action='store_const', const=True, default=False)
    
    # Parsing proper:
    args = parser.parse_args()
    #print(args) ; return
    
    #################################################
    ##### Semantic checks:        ###################
    #################################################
    matching_modes = get_cmdline_semantics(
        args = args,
        modes = [
            (['run_lib_tests', ],
                lambda args: op_run_lib_tests(),
                "Run deb-building-library tests.",
                ),
            ],
        )
    
    #######################################################
    ##### Do the payload itself:        ###################
    #######################################################
    matching_modes[0][1](args)

if __name__ == "__main__": Main()
