#!/usr/bin/python

# CSVtoHDLsim.py by Marek Pikuła <marek a pikula d co>
# Published under GNU GPLv3 license

import argparse
import csv

parser = argparse.ArgumentParser(description='Parse CSV to HDL simulation code.\n\nThere should be timestamp in first column and signals in next columns, with signal names in first row.')
parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
parser.add_argument('-l', '--lang', help='Select output language', choices=['VHDL'], default='VHDL')
parser.add_argument('--dialect', '-d', metavar='DIALECT', help='Set dialect of CSV file (for csv.reader)')
parser.add_argument('--time', '-t', metavar='UNIT', help='Set time unit for first column (in language specific notation)', default='sec')
parser.add_argument('file', help='CSV file to parse', type=argparse.FileType('rb'))
args = parser.parse_args()

src = csv.reader(args.file, dialect=args.dialect)
firstRow = src.next()
lastRow = [0] * len(firstRow)
timeAcc = 0.0
for row in src:
    if float(row[0]) >= 0:  # ignore negative time stamps
        wait = False
        timeAcc += float(row[0]) - float(lastRow[0]) # Accumulate time for constant signals
        for n in range(1, len(row)):
            if int(row[n]) != int(lastRow[n]): # Check if any value has changed
                if not wait:
                    if args.lang == 'VHDL':
                        print 'wait for ' + ("{:10.4E}".format(timeAcc)) + ' ' + args.time + ';'
                    timeAcc = 0.0
                    wait = True
                
                # Assigment operation
                if args.lang == 'VHDL':
                    print firstRow[n] + '<=\'' + str(int(row[n])) + '\';'
        lastRow = row
