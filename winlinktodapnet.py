#!/usr/bin/env python
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Author: Raffaello Di Martino IZ0QWM
# Date: 15.08.2018
# Version 0.1

import logging
import time
import sched
from time import sleep
from datetime import datetime
import urllib2
import urllib3
import json
import base64
import math
import threading
from threading import Timer
import thread
import re
import sys
import configparser
import os
import requests
import websocket
import string
from random import randint

# Leggo il file di configurazione
cfg = configparser.RawConfigParser()
try:
        #attempt to read the config file winlinktodapnet.cfg
        config_file = os.path.join(os.path.dirname(__file__),'winlinktodapnet.cfg')
        cfg.read(config_file)
except:
        #no luck reading the config file, write error and bail out
        logger.error('winlinktodapnet could not find / read config file')
        sys.exit(0)

#logging.basicConfig(filename='dapaprsgate.log',level=logging.INFO) # level=10
logger = logging.getLogger('dapnet')
handler = logging.FileHandler('winlinktodapnet.log')
logformat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(logformat)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Leggo le credenziali per WINLINK
winlinkusername = cfg.get('user','username')
winlinkpassword = cfg.get('user','password')
hampagerurl = cfg.get('dapnet','baseurl') + cfg.get('dapnet','coreurl')
