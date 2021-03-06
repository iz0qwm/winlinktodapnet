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

import logging
import urllib2
import urllib3
import time
from time import sleep
from datetime import datetime
import sys
import configparser
import os
import requests
import string
import telnetlib
import subprocess
version = subprocess.check_output(["git", "describe"]).strip()

# Leggo il file di configurazione
cfg = configparser.RawConfigParser()
try:
    # attempt to read the config file winlinktodapnet.cfg
    config_file = os.path.join(os.path.dirname(__file__), 'winlinktodapnet.cfg')
    cfg.read(config_file)
except:
    # no luck reading the config file, write error and bail out
    print(os.path.basename(__file__) + " could not find / read config file")
    sys.exit(0)

# Leggo la posizione del logfile
logfile = cfg.get('misc', 'logfile')

# logging.basicConfig(filename='winlinktodapnet.log',level=logging.INFO) # level=10
logger = logging.getLogger('wlnk2dapnet')
handler = logging.FileHandler(logfile)
logformat = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(logformat)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Leggo le credenziali per WINLINK
winlinkusername = cfg.get('winlink', 'username')
winlinkpassword = cfg.get('winlink', 'password')
winlinkhost = cfg.get('winlink', 'host')
winlinkport = cfg.get('winlink', 'port')
winlinkpassfirst = "CMSTELNET"

# Leggo le credenziali per DAPNET
hampagerusername = cfg.get('dapnet','user')
hampagerpassword = cfg.get('dapnet','password')
hampagerurl = cfg.get('dapnet','baseurl') + cfg.get('dapnet','coreurl')
hampagegroup = cfg.get('dapnet','transmittergrp')

tn = telnetlib.Telnet()
# tn.set_debuglevel(10)
tn.open(winlinkhost, int(winlinkport))
logger.info('winlinktodapnet %s engaged...', version)
logger.info('------------------')
logger.info('Inizio sessione')
# Login con password CMSTELNET
tn.read_until("Callsign :",5)
tn.write(winlinkusername.encode('ascii') + b"\r")
if winlinkpassfirst:
    tn.read_until("Password :",5)
    tn.write(winlinkpassfirst.encode('ascii') + b"\r")
tn.read_until("CMS>\r", 5)
# Invio qualsiasi comando per ricevere la richiesta di challenge
tn.write("LM\r")
# Interpreto la richiesta Es. Login [564] - Dove 564 sono le posizioni delle lettere della
# password ad iniziare da 1
login = tn.expect([r"Login [[0-9][0-9][0-9][0-9]"], 5)
login_completo = login[2]
login_password = login_completo[7:10]
lettera1 = login_password[0:1]
lettera2 = login_password[1:2]
lettera3 = login_password[2:3]
logger.info('Posizione1: %s - Posizione2: %s - Posizione3: %s', lettera1, lettera2, lettera3)
#print lettera1
#print lettera2
#print lettera3
for index, char in enumerate(winlinkpassword):
    if index+1 == int(lettera3):
        carattere_lettera3 = char
    if index+1 == int(lettera2):
        carattere_lettera2 = char
    if index+1 == int(lettera1):
        carattere_lettera1 = char

logger.info('Carattere1: %s - Carattere2: %s - Carattere3: %s', carattere_lettera1, carattere_lettera2, carattere_lettera3)
# In piu si aggiungono altri tre caratteri
caratteri_da_inviare = carattere_lettera1 + carattere_lettera2 + carattere_lettera3 + "ABC"
logger.info('Invio la password challenge: %s', caratteri_da_inviare)
#print caratteri_da_inviare
tn.read_until("CMS>\r", 5)
tn.write(caratteri_da_inviare.encode('ascii') + b"\r")
tn.read_until("CMS>\r", 5)
tn.write("LM\r")
# Leggo i messaggi nuovi
intestazione = tn.read_until("\r")
if intestazione.find("No pending messages") == -1:
    # Invio messaggio -> DAPNET
    # create the complete URL to send to DAPNET
    messaggio_ctrlm = intestazione[13:]
    messaggio = messaggio_ctrlm.replace(r'\r','')
    logger.info('Intestazione: %s', messaggio)
    http = urllib3.PoolManager()
    headers = urllib3.util.make_headers(basic_auth= hampagerusername + ':' + hampagerpassword)
    da = "WINLINK"
    payload = '{ "text": "'+ da +': ' + messaggio +'", "callSignNames": [ "' + hampagerusername + '" ], "transmitterGroupNames": [ "' + hampagegroup + '" ], "emergency": false}'

    try:
        # try to establish connection to DAPNET
        response = requests.post(hampagerurl, headers=headers, data=payload)
    except:
        # connection to DAPNET failed, write warning to console, write warning to error log then bail out
        logger.error('Invalid DAPNET credentials or payload not well done')
        sys.exit(0)
    else:
        # connection to DAPNET has been established, continue
        logger.info('-------------------------------------------')
        logger.info('MESSAGGIO INVIATO SU DAPNET')
        logger.info('-------------------------------------------')
else:
    logger.info('Intestazione: %s', intestazione[13:])
    logger.info('Non invio nulla su pager')
# Continuo e chiudo la comunicazione
tn.read_until("CMS>\r", 5)
tn.write("bye\r")
logger.info('Fine sessione')
logger.info('------------------')


