#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import types
import sys
from time import sleep, time
import readchar



while (True):
    try:
        sleep(0.1)
        rfid_input = str(raw_input('rfid input:')) # python2: raw_input; python3: input
        if(rfid_input == 'x'):
            break
        else:
            print("input was: " + rfid_input)

    except KeyboardInterrupt: #Strg-C wird gedrückt
        print("Exception raised.")


