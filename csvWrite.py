import csv
import os.path
import datetime

outputFile = "C:\Users\\antth\PycharmProjects\csvTest\\" + datetime.datetime.now().strftime("%m_%d_%Y") + ".csv"

soapNum = 4
waterNum = 1
date = datetime.datetime.now().strftime("%m_%d_%Y")

def writeToCSV():
    if os.path.exists(outputFile) is True:
        with open(outputFile, 'ab') as outcsv:
             writer = csv.writer(outcsv)
             writer.writerow([date, waterNum, soapNum])
        print("Wrote to file")

    else:
        with open(outputFile, 'wb') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(['Date-Time', 'Number of Water Events', 'Number of Soap Events'])

        print("Created file")

writeToCSV()
