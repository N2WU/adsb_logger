#!/usr/bin/env/python3
#import gpsd
#import picamera
import time
from subprocess import run,call
from datetime import datetime
import csv
import os
import socket

CSVHeaders = ["Index", "Type", "MSG Type", "Session ID", "Aircraft ID",
            "ModeS Hex", "FlightID", "Date gen", "Time gen",
            "Date logged", "Time logged", "Callsign", "Altitude", "Ground Speed",
            "Track", "Lat", "Lon", "VerticalRate", "Squawk", "Alert", "Emergency",
            "SPI", "IsOnGround"]

with open('data.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(CSVHeaders)

def readTCP():
    separator=("\n")
    try:
        host_ip = "127.0.0.1"
        server_port = 30005 #receive decoded messages
        # Establish connection to TCP server and exchange data
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((host_ip, server_port))
        # Read data from the TCP server and close the connection
        received = tcp_client.recv(1024)
    finally:
        tcp_client.close()
    receivedData = received.decode()
    packet = receivedData.split("\n")[0] #just in case, we don't want two packets
    return packet


def writeCSV(index, packet):
    #timenow = datetime.now()
    # stringTime = timenow.strftime("%Y.%m.%d-%H%M%S")
    #parse incoming decoded packets into an array
    #example packet: MSG,4,5,211,4CA2D6,10057,2008/11/28,14:53:49.986,2008/11/28,14:58:51.153,,,408.3,146.4,,,64,,,,,
    packet_list = packet.split(",") #now it should be 22 items long
    Row = [index,  packet_list]
    with open(r'data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(Row)



index = 0


if __name__ == '__main__':

    packet = readTCP()

    writeCSV(index, packet)
    index += 1

    time.sleep(2)
