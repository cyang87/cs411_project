import csv
import sys

openFile = open('data2.csv', 'r')
csvFile = csv.reader(openFile)
headers = next(csvFile)
headers = [str(header) if i == 0 else 'Y' + str(header) for i, header in enumerate(headers)]
outFile = open('data2.sql', 'w')

outFile.write('CREATE TABLE pop (' + headers[0] + ' VARCHAR(20) NOT NULL PRIMARY KEY')
for i in range(1, len(headers)):
    outFile.write(', ' + headers[i] + ' INTEGER NOT NULL')
outFile.write(');\n')

outFile.write('INSERT INTO pop (' + ", ".join(headers) + ') VALUES ')
for values in csvFile:
    values = ["'" + str(value) + "'" if i == 0 else str(value) for i, value in enumerate(values)]
    outFile.write("(" + ", ".join(values) +"),\n")
openFile.close()
outFile.close()