#!/usr/bin/python3

import configparser
import sys, getopt
import os.path
from os import path

def main(argv):
    config_file = ''
    if(len(argv) < 1):
        print('Usage: python3 check.py -c <configure_file>')
        sys.exit(3)
    try:
        opts, args = getopt.getopt(argv,"c:",["cfile="])
    except getopt.GetoptError:
        print('Usage: python3 check.py -c <configure_file>')
        sys.exit(2)
    for opt, arg in opts:
        if (opt in ("-c", "--cfile")):
            config_file = arg
    print("Using configuration file {}".format(config_file))
    config = configparser.ConfigParser()
    config.read(config_file)
    if('DEFAULT' not in config):
        print('Wrong configuration format.')
        sys.exit(4)
    
    inputsource = config['DEFAULT']['input']
    outputexe = config['DEFAULT']['output']
    makercmd = config['DEFAULT']['maker']
    verifier = config['DEFAULT']['verifier']

    print("Input source codes: {}".format(inputsource))
    print("Verifying program: {}".format(verifier))
    
    if(path.exists(outputexe)):
        print("Previous compiled program exists. Deleting...")
        os.remove(outputexe)

    #Compile
    print("Compiling {}...".format(inputsource))
    os.system(makercmd)
    if(path.exists(outputexe) == False):
        print("Failed in compile.")
        sys.exit(5)
    print("\"{}\" is generated.".format(outputexe))

    #Running
    print("Running \"{} {}\"".format(outputexe,config['INPUTPARAMS']['in1']))
    stream1 = os.popen("./{} {}".format(outputexe,config['INPUTPARAMS']['in1']))
    output1 = stream1.read()
    print(output1)

    #Verifying
    print("Running verifier \"{}\"".format(verifier))
    stream2 = os.popen("{}".format(verifier))
    output2 = stream2.read()
    print(output2)

    if(output2 == output1):
        print("Results matched.")
    else:
        print("Results didn't match.")

if __name__ == "__main__":
    main(sys.argv[1:])

