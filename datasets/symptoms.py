import csv
import sys

openFile = open('symptoms.csv', 'r')
csvFile = csv.reader(openFile)
headers = next(csvFile)
headers = ['SymptomID', 'Name']
outFile = open('symptoms.sql', 'w')

outFile.write(
    'CREATE TABLE symptoms (' + headers[0] + ' INTEGER NOT NULL PRIMARY KEY, ' + headers[1] + ' TEXT NOT NULL);\n')

outFile.write('INSERT INTO symptoms (' + ", ".join(headers) + ') VALUES ')
for values in csvFile:
    values = ["'" + str(value) + "'" if i == 1 else str(value) for i, value in enumerate(values)]
    values = [value.replace("'s", "''s") for value in values]
    values = [value.replace("\v", "") for value in values]
    values = [value.replace("s' ", "s ") for value in values]
    outFile.write("(" + ", ".join(values) +"),\n")
openFile.close()
outFile.close()