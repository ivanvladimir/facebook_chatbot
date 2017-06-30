#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import aiml
import sys
import argparse

# Función principal (interfaz con línea de comandos)
if __name__ == '__main__':
    p = argparse.ArgumentParser("commandline")
    p.add_argument("AIML",type=str,
            action="store",
            help="AIML file with rules [aiml/mibot.aiml]")

    opts = p.parse_args()

    k=aiml.Kernel()

    # The Kernel object is the public interface to
    # the AIML interpreter.
    k = aiml.Kernel()

    # Use the 'learn' method to load the contents
    # of an AIML file into the Kernel.
    k.learn(opts.AIML)

    # Loop forever, reading user input from the command
    # line and printing responses.
    while True: print(k.respond(raw_input("> ")))
