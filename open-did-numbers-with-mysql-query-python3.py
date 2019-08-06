#!/usr/bin/python3

# Written by github.com/stolig
# query shoretel db and find out which extensions and DID's can be used.
# update your mysql db username and pwd in this script.
# make sure you have the mysql connector installed
# extension ranges are defined in your shoretel system.
# update fax list in the faxList array if you're excluding fax numbers that may be in use. 

from sys import argv
import mysql.connector

d1 = {}

def findDid():

    listExt = []
    listDid = []
    listRange5500 = []
    listRange5840 = []
    listRange5900 = []

    faxList = [5902,5926,5928,5929,5930,5931,5932,5933,5934,5935,5936,5937,5938,5939,5940,5941,5942,5943,5944,5945,5946]

    for eachLine in d1.items():

        myExt = eachLine[0]
        myDid = eachLine[1]

        listExt.append(myExt)

        if myDid:

            listDid.append(myDid[-4:])

    listExt = set(listExt)

    listDid = set(listDid)

# Check in each range:

    for rangeItem in range(5500,5599):

        rangeItem = str(rangeItem)
        listRange5500.append(rangeItem)

    listRange5500 = set(listRange5500)

    diffRange5500 = listRange5500.difference(listExt) 
    diffDID5500 = listRange5500.difference(listDid)

    for rangeItem in range(5840,5899):
        
        rangeItem = str(rangeItem)
        listRange5840.append(rangeItem)

    listRange5840 = set(listRange5840)

    diffRange5840 = listRange5840.difference(listExt) 
    diffDID5840 = listRange5840.difference(listDid)

    for rangeItem in range(5900,5999):

        if rangeItem not in faxList: 
        
            rangeItem = str(rangeItem)
            listRange5900.append(rangeItem)

    listRange5900 = set(listRange5900)

    diffRange5900 = listRange5900.difference(listExt) 
    diffDID5900 = listRange5900.difference(listDid)

    print("*" * 50)
    print("\nExtensions that are not being used:\n")
    print("*" * 50)
    print("\n5550 Range: ", len(diffRange5500), "\n")
    print(sorted(diffRange5500))
    print("\n5840 Range: ", len(diffRange5840), "\n")
    print(sorted(diffRange5840))
    print("\n5900 Range: ", len(diffRange5900), "\n")
    print(sorted(diffRange5900))
    print("\n")

    print("*" * 50)
    print("\nDID's that are not being used:\n")
    print("*" * 50)
    print("\n5550 Range: ", len(diffDID5500), "\n")
    print(sorted(diffDID5500))
    print("\n5840 Range: ", len(diffDID5840), "\n")
    print(sorted(diffDID5840))
    print("\n5900 Range: ", len(diffDID5900), "\n")
    print(sorted(diffDID5900))
    print("\n")

def queryShoretel():

    cnx = mysql.connector.connect(user='myuser', password='mypassword', database='shoreware', host='your-director-server', port=4308)

    cursor = cnx.cursor()

    query = ("SELECT DN, Digits FROM systemdirectorydisplay ")

    cursor.execute(query)

    for row in cursor:

        for item in row:

            shoretelExt = row[0]
            shoretelDid = row[1]

            d1[shoretelExt] = shoretelDid

    cursor.close()
    cnx.close()

    findDid()

queryShoretel()
