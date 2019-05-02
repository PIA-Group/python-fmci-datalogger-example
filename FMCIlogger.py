# -*- coding: utf-8 -*-
"""
Connects to the serial port, that is in contact with the FMCI device
Receives its information and stores it in a txt file, with three columns
    Time since the acquisition began 
    GSR value at the time
Stores errors in a txt file

"""

# Imports
import serial
import time
import numpy as np
from datetime import datetime
import serial.tools.list_ports as sr

# Variables declaration
DATETIME = datetime.now()
DATETIME = str(DATETIME.year) + str(DATETIME.month) + str(DATETIME.day) + '_' + str(DATETIME.hour) + str(DATETIME.minute)
known_ids = []
BAUDRATE = 115200
t0 = None


def createlogfile(DATETIME):
    t0=time.time()
    f=port.readline()
    l=f.decode('utf-8').split(',')
    datalog=open(str(DATETIME) + '_FMCI_LOG.txt', 'w')
    datalog.write('# Timestamp\t' + 'Log' + '\n')
    datalog.write(str(np.round(time.time() - t0, 3)) + '\t' + l[0][2:-2])
    datalog.close()
    f=port.readline()
    return t0


def createFMCIfile(DATETIME, t0, known_ids, f):
    l=f.decode('utf-8').split(',')
    known_ids.append(l[0])
    data = open(str(DATETIME) + '_FMCI' + '_' + str(known_ids[-1]) + '.txt', 'w')
    data.write('# Timestamp\t' + 'GSR\t' + 'TIMESTAMP REAL:' + str(t0) + '\n')
    data.close()
    return known_ids


def get_port():
    portsCOM = []
    portsAdd = []
    for port_no, description, add in list(sr.comports()):
        if 'USB' in description:
            portsCOM.append(port_no)
            portsAdd.append(add)
    if len(portsCOM) > 1:  # If more than 1 USBs are connected to the computer
        print('Selection oF FMCI serial port (Select one)')
        for i in range(len(portsCOM)):
            print('Available Ports: ' + str(i) + '\n')
        print('Selected USB: ')
        try:
            user_input = int(input())
        except:
            print('Please type one of the options')
        PORT = portsCOM[user_input]
    else:  # If only one USB port is connected
        PORT = portsCOM[0]
    return PORT


if __name__ == '__main__':
    PORT = get_port()
    try:
        port = serial.Serial(PORT, BAUDRATE)
        port.flushInput()
        t0 = createlogfile(DATETIME)
        f = port.readline()
        known_ids = createFMCIfile(DATETIME, t0, known_ids, f)
        while 1:
            f = port.readline()
            l = f.decode('utf-8').split(',')
            if len(l) == 2:  # Ensures it is GSR data
                if l[0] not in known_ids:
                    known_ids = createFMCIfile(DATETIME, t0, known_ids, f)
                data = open(str(DATETIME) + '_FMCI' + '_' + str(l[0]) + '.txt','a')
                data.write(str(np.round(time.time() - t0, 3)) + '\t' + str(l[1][:-2]))
                data.write('\n')
                data.close()
            else:
                datalog = open(str(DATETIME) + '_FMCI_LOG.txt', 'a')
                datalog.write(str(np.round(time.time() - t0, 3)) + '\t' + str(l))
                datalog.close()
    finally:
        port.close()

    

