# SiglentSDS1204X-E

## Purpose

Pull waveforms from Siglent scope by taking advantage of online feature, to circumvent need for VISA front and backends.

Rather than using LAN communication to collect data, which is slow with the Siglent scope, this program uses a webdriver to open the net interface of the scope. The program will push buttons in the web interface to control the scope. On single trigger mode, the program will check the trigger status at about 10 Hz. At any instance where the scope has been triggered, it will take a screenshot of the waveform and store it in a directory. A data file will be generated with the time stamp and trigger status of each check. A few parameters, like time and voltage divs, will be obtained over LAN communication using a socket. The socket is severed when data acqusition begins to reduce fatal errors. 

Once acquisiton is done, CSV's of the waveforms can be generated using the acquired screenshots. 

## Program Configuration and Requirements 

### Device Requirements
Program is meant to be run on Mac OS. Scope needs to be powered on and connected to localhost. Mac device nees to be connected to localhost. 

This program only reads data from CH1. The view on the scope must be set to channel 1, so that the whole ch1 waveform is visible. 

On the scope, Utility -> I/O --> IP Set --> DHCP needs to be on. 

This is a python3 program.
### Installation 
Message me with a public key for cloning. Once given access, running "Installation.sh" from the command line of a Mac terminal will check the system, get the appropriate libraries, and clone the SiglentSDS1204x-E repository. 

Once the zip resulting from cloning, it will open a directory. In that directory, run "config_chromedriver.sh" to add chromedriver to path so that selenium may use it. The zip for Chrome 84 on MacOS is inlcuded in the repo. For different versions of chrome, remove the included zip and replace with the driver for the appropriate version. The configuration shell script will unzip any version, and add the driver to "/usr/local/bin", which should already be on $PATH. Restart shell, and then the repo should be ready for use. 

To run: ./RollingAcq_scrn.py <IP> <RunTime>
  
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
Library for acqusition of waveform screenshots, configuration of scope, acqusition of initial conditions, trigger control.
Class format. 

**ReadFile(infile):** read lines of a file

**checkargs():** exit program if correct number of command line arguements is not given, return arguements

**getArgs():** extract IP and run time from command line arguements
- output is list: [\<IP\>, \<RunTime\>]
  
**checkdir():** check existing directories to assign sequential experiment numbers

**ConfigOutput():** run checkdir
- return list: <out file>, <experiment number>
  
**mkdir():** Setup configurations for experiment and make experimental directory
- output is name of directory 

**StartLog(dir, xdiv, ydiv):** Log experiment, initial

**EndLog(StartTime, n, i):** Finish logging experiment 
- n is number of waveforms collected 
- i is number of times trigger was checked

**SocketConnect(IP, port):** make socket to interface with scope

**SocketClose():** close socket

**SocketQuery(cmd):** send query to socket, get reply
- return reply to query

**TrigStat():** check status of trigger over socket
- return reply to trigger status query, recieved over socket

**TimeDivs():** check time divisions
- return time divs, time div units

**VoltDivs():** check volt divisions
- return voltdivs, volt div units

**GoToInstrWebPage(IP):** open chrome to web interface page

**Button_WfmBin():** locate button that saves binary waveform

**Button_RunStop()**: Find Run/Stop Button

**Button_SidePanel():** Find side panel button 

**Button_Single():** Find Single trigger button

**Button_ScreenSave():** Find screensave button

**OpenSidePanel():** press button to open side panel

**FindAllButtons():** locate all the buttons you will need for the rest of the program

**PressSingle():** Press button to reset in single trigger mode

**CheckTriggerButton():** Check the color of the Run/Stop button, triggered if red. 
- return 'STOP' if red
- return 'RUN' if green

**GetBinWf():** download binary waveform (takes about 10s)

**ScreenGrab(i):** save screenshot of driver with waveform as png numbered by iteration

**GetBMP():** save screendump of waveform using built in feature on web interface

**QuitDriver():** quit chromedriver

**Collect(st, rt, df):** Collect screenshots of driver 
- will check trigger at rate of about 10 Hz.
  - if triggered, will collect screenshot and then reset trigger
  - if not triggered, record check and loop again 
- will go until run time is expired
### ExtractWfm.py 

This file contains functions necessary to extract the Channel 1 waveform from a screenshot of the net interface to generate a csv. It assumes that each div is 50 pixels wide, which works for the Macbook Air I developed it on. It is easy to check if this is the same on other devices 

**open_png(path):** open image with described path in PIL library for use

**get_pixel(img, i, j):** get the rgb value of the pixel at i, j in img
- return True if the value indicates it is on the waveform displayed for ch1
- return False if the rgb does not match the ch1 waveform value

**get_black(img, i, j):** test function that picks out all the black pixels

**get_wfm(img):** check every pixel in img
- return indexed list of x, y values which represent pixels on the waveform (rgb matches the yellow color that the scope displayes ch1 in)

**plt_black(img):** return list of black pixels  (for test purposes)

**cleanup(img, t, v):** average values to give single valued function 
- takes the image, x, and y pixels from the waveform as inputs. t, v is x, y pixels. t, v should be output of get_wfm. 
- averages all the voltage values collected for each time value so that cleaned up waveform is returned 
- returns time, volt arrays with matching indexes

**GetDat(xdiv, ydiv, time, volts):** convert the pixel values to voltage and time values by going from pixels to scope devisions. output is x, y arrays which have been scaled properly to x, y div value (get units from SDS1204XE.py)
- xdiv, ydiv are the numerical values for time, voltages per division (50 p) on the scope window. Take note of units, but this function does not take units into account. 
- time, voltages should be the arrays which were outputs from cleanup(img, t, v)

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

