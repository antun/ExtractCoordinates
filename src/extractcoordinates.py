#!/usr/bin/python

import os, sys, inspect, argparse, subprocess, re

# identify -verbose /Users/antun/Desktop/LA\ Pics/20121123_122755.jpg  | egrep 'Latit|Long'
# exif:GPSAltitude: 0/1000
# exif:GPSAltitudeRef: 0
# exif:GPSDateStamp: 2012:11:23
# exif:GPSInfo: 4898
# exif:GPSLatitude: 34/1, 0/1, 29948/1000
# exif:GPSLatitudeRef: N
# exif:GPSLongitude: 118/1, 29/1, 39001/1000
# exif:GPSLongitudeRef: W
# exif:GPSTimeStamp: 20/1, 27/1, 46/1
# exif:GPSVersionID: 2, 2, 0, 0

def coordinatesToDecimal(degrees, minutes, seconds):
    # Convert to decimal
    minutes += (seconds / 60)
    degrees += (minutes / 60)
    return degrees

def getLatitude(exif):
    m = re.search('exif:GPSLatitude: (.+)/(.+), (.+)/(.+), (.+)/(.+)', exif)
    degrees = float(m.group(1)) / float(m.group(2)) 
    minutes = float(m.group(3)) / float(m.group(4)) 
    seconds = float(m.group(5)) / float(m.group(6)) 
    degrees = coordinatesToDecimal(degrees, minutes, seconds)
    m = re.search('exif:GPSLatitudeRef: ([NS])', exif)
    northSouth = 1
    if m.group(1) == 'S':
        northSouth = -1
    degrees *= northSouth
    return degrees

def getLongitude(exif):
    m = re.search('exif:GPSLongitude: (.+)/(.+), (.+)/(.+), (.+)/(.+)', exif)
    degrees = float(m.group(1)) / float(m.group(2)) 
    minutes = float(m.group(3)) / float(m.group(4)) 
    seconds = float(m.group(5)) / float(m.group(6)) 
    degrees = coordinatesToDecimal(degrees, minutes, seconds)
    m = re.search('exif:GPSLongitudeRef: ([EW])', exif)
    eastWest = 1
    if m.group(1) == 'W':
        eastWest = -1
    degrees *= eastWest
    return degrees

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extracts GPS and basic EXIF information into an XML file.')
    parser.add_argument('filename', help='Excel (xls or xlsx) file.')
    args = parser.parse_args()
    exif = subprocess.check_output(["identify", "-verbose", args.filename])
    latitude = getLatitude(exif)
    longitude = getLongitude(exif)
    print "<image filename=\""+args.filename+"\">"
    print "<coordinates value=\""+str(latitude) + "," + str(longitude)+"\" />"
    print "</image>"
    
