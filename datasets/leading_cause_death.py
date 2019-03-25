import csv
import sys

openFile = open('leading_cause_death.csv', 'r')
csvFile = csv.reader(openFile)
headers = next(csvFile)
headers = ['C' + str(header) if i == 1 else str(header) for i, header in enumerate(headers)]
outFile = open('leading_cause_death.sql', 'w')

outFile.write('CREATE TABLE causes (' + headers[0] + ' INTEGER NOT NULL')
outFile.write(', ' + headers[1] + ' TEXT NOT NULL')
for i in range(2, 4):
    outFile.write(', ' + headers[i] + ' VARCHAR(100) NOT NULL')
outFile.write(', ' + headers[4] + ' INTEGER')
outFile.write(', ' + headers[5] + ' REAL')
outFile.write(', ' + 'CONSTRAINT Pk PRIMARY KEY (' + ",".join([headers[0], headers[2], headers[3]]) + ')' )
outFile.write(');\n')

outFile.write('INSERT INTO causes (' + ", ".join(headers) + ') VALUES ')
for values in csvFile:
    values = ["'" + str(value) + "'" if (i >= 1 and i <= 3) else str(value) for i, value in enumerate(values)]
    values = [value.replace("'s", "''s") for value in values]
    values = ["NULL" if (value == "*" or value == "x") else value for value in values]
    outFile.write("(" + ", ".join(values) +"),\n")
openFile.close()
outFile.close()