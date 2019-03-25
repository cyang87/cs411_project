import csv
import sys

openFile = open('mapping.csv', 'r')
csvFile = csv.reader(openFile)
headers = ['DiseaseID', 'Name']
outFile = open('mapping.sql', 'w')

outFile.write(
    'CREATE TABLE mapping (' + headers[0] + ' INTEGER NOT NULL PRIMARY KEY, ' + headers[1] + ' TEXT NOT NULL);\n')

outFile.write('INSERT INTO mapping (' + ", ".join(headers) + ') VALUES ')
for values in csvFile:
    values = ["'" + str(value) + "'" if i == 1 else str(value) for i, value in enumerate(values)]
    outFile.write("(" + ", ".join(values) +"),\n")
openFile.close()
outFile.close()