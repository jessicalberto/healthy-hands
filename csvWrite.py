import csv
import os.path
import datetime

outputFile = "C:\Users\\antth\PycharmProjects\csvTest\\" + datetime.datetime.now().strftime("%m_%d_%Y") + ".csv"

def writeToCSV():
    if os.path.exists(outputFile) is True:
       print("write to file")
    else:
        with open(outputFile, 'wb') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(['Date-Time', 'Number of Water Events', 'Number of Soap Events'])
        print("Now write to file")
writeToCSV()
