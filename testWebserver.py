#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import types
import sys
from socket import error as SocketError
import mpd
#import mpc  # ?
from time import sleep, time
import RPi.GPIO as GPIO
import readchar
from flask import Flask
from flask import jsonify

print ("Setting constants...")

global TEST_MPD_HOST, TEST_MPD_PORT, TEST_MPD_PASSWORD

TEST_MPD_HOST = "localhost"
TEST_MPD_PORT = "6600"
TEST_MPD_PASSWORD = ""
POWEROFF_TIME = 10

OUT_PIN_POWER = 3

IN_PIN_VOLUME_UP = 12
IN_PIN_VOLUME_DOWN = 13
IN_PIN_TRACK_NEXT = 15
IN_PIN_TRACK_PREVIOUS = 16
IN_PIN_TOGGLE_PLAY_PAUSE = 11

print ("...done!")


app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(result='Hello World')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")