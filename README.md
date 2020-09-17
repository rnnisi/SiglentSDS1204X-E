# SiglentSDS1204X-E

## purpose

Pull waveforms from Siglent scope by taking advantage of online feature, to circumvent need for VISA front and backends.

Rather than using LAN communication to collect data, which is slow with the Siglent scope, this program uses a webdriver to open the net interface of the scope. The program will push buttons in the web interface to control the scope. On single trigger mode, the program will check the trigger status at about 10 Hz. At any instance where the scope has been triggered, it will take a screenshot of the waveform and store it in a directory. A data file will be generated with the time stamp and trigger status of each check. A few parameters, like time and voltage divs, will be obtained over LAN communication using a socket. The socket is severed when data acqusition begins to reduce fatal errors. 

Once acquisiton is done, CSV's of the waveforms can be generated using the acquired screenshots. 

## Program Configuration and Requirements 

### Device Requirements
Program is meant to be run on Mac OS. Scope needs to be powered on and connected to localhost. Mac device nees to be connected to localhost. 

On the scope, Utility -> I/O --> IP Set --> DHCP needs to be on. 

This is a python3 program.

### Python libraries 
- time 
- selenium 
- sys
- socket
- os
- subprocess
- PIL
- numpy

### Driver
- chromedriver (make sure path is properly configured for python 3)

## Contents
### SDS1204XE.py
library for acqusition of waveform screenshots, configuration of scope, acqusition of initial conditions, trigger control.

### ExtractWfm.py 
generates CSV from screenshot of scope face

### RollingAcq_scrn.py
Data acqusition and automatic generation of csv's. Expects three arguements: ./RillingAcq_scrn.py [IP of scope] [Acq time in seconds]

### LOG.txt
Each run will be recorded in this log with a time stamp, run time, number of trigger checks, number of waveforms collected.

### plot.py
Plots waveform csv. Takes n (as in ScreenDump_n.csv) as arguement. Use in Exp_N directory. 

## Outputs 
### Trigger Checks: Exp_n.txt
This file has one line for each trigger check. If the scope is triggered, the line will start with "TRIGGERED", followed by 'i', which is the iteration, and then time, which is the time of check. t = 0 is initialization

### Data: Screenshots and CSV's
For each experiment, a directory will be created. All the screenshots will be saved in this file, labeled by the iteration number. CSV's will also be saved in this directory 

