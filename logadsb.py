#!/usr/bin/env/python3
#import gpsd
#import picamera
import time
from subprocess import run,call
from datetime import datetime
import csv
import os
import RPi.GPIO as GPIO
from pyModeS.decoder import adsb
import socket

GPIO.setmode(GPIO.BCM)
# Initialize a TCP client socket using SOCK_STREAM

# Connect to the local gpsd
# maybe in the future
"""
try:
    gpsd.connect()
except:
   command = "sudo gpsd /dev/serial0 -F /var/run/gpsd.sock"
   run([command, -l])
finally:
   gpsd.connect()
"""
#gpsd.connect(host="127.0.0.1", port=1234)

# Get gps position
# packet = gpsd.get_current()

# See the inline docs for GpsResponse for the available data
# print(packet.position())
# icao,callsign,velocity,pos_with_ref,vel2
CSVHeaders = ["Index", "Time", "ICAO", "Callsign", "Velocity", "Position With Reference", "Velocity 2"] 

with open('data.csv', 'w') as f: 
    write = csv.writer(f) 
    write.writerow(CSVHeaders) 

def readTCP():
    separator=("\n")
    try:
        host_ip = "127.0.0.1"
        server_port = 30002
        # Establish connection to TCP server and exchange data
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()
    receivedData = received.decode()
    rawData = receivedData.split(separator)
    return rawData



def getADSBData(msg):
    icao = pms.adsb.icao(msg)
    pms.adsb.typecode(msg)

    # Typecode 1-4
    callsign = pms.adsb.callsign(msg)

    # Typecode 5-8 (surface), 9-18 (airborne, barometric height), and 20-22 (airborne, GNSS height)
    pms.adsb.position(msg_even, msg_odd, t_even, t_odd, lat_ref=None, lon_ref=None)
    pms.adsb.airborne_position(msg_even, msg_odd, t_even, t_odd)
    pms.adsb.surface_position(msg_even, msg_odd, t_even, t_odd, lat_ref, lon_ref)
    velocity = pms.adsb.surface_velocity(msg)

    pos_with_ref = pms.adsb.position_with_ref(msg, lat_ref, lon_ref)
    pms.adsb.airborne_position_with_ref(msg, lat_ref, lon_ref)
    pms.adsb.surface_position_with_ref(msg, lat_ref, lon_ref)

    altitude = pms.adsb.altitude(msg)

    # Typecode: 19
    vel2 = pms.adsb.velocity(msg)          # Handles both surface & airborne messages
    pms.adsb.speed_heading(msg)     # Handles both surface & airborne messages
    pms.adsb.airborne_velocity(msg)
    
    flightInfo = [icao,callsign,velocity,pos_with_ref,altitude,vel2]
    
    return flightInfo

"""
def getPositionData():
    packet = gpsd.get_current()
    latlonString = packet.position()
    return latlonString
"""
def writeCSV(gpsData, index, flightInfo):
    timenow = datetime.now()
    stringTime = currentTime.strftime("%Y.%m.%d-%H%M%S")
    Row = [index, stringTime, flightInfo[0], flightInfo[1], flightInfo[2],flightInfo[3], flightInfo[4], flightInfo[5]]
    with open(r'data.csv', 'a') as f:
        writer = csv.writer(f)



indexTotal = 50
index = 0


if __name__ == '__main__':
    # Grab the current time
    currentTime = datetime.now()
    #gpsData = getPositionData()
    # improve since packet is now an array of msgs
    packet = readTCP()
    for i in packet:
        flightInfo = getADSBData(packet)
        writeCSV(index, currentTime, flightInfo)
        index += 1
    # Write csv
    #flightInfo = getNewADSB()
    """
    if len(flightInfo) > 0:
        writeCSV(index, currentTime, flightInfo)
        print("Written to CSV")    
        index += 1
    """
    time.sleep(2)         
