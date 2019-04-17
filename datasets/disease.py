import csv
import sys

openFile = open('disease.csv', 'r')
csvFile = csv.reader(openFile)
headers = next(csvFile)
headers = ['DiseaseID', 'Name']
outFile = open('disease.sql', 'w')

outFile.write(
    'CREATE TABLE disease (' + headers[0] + ' INTEGER NOT NULL PRIMARY KEY, ' + headers[1] + ' TEXT NOT NULL);\n')

outFile.write('INSERT INTO disease (' + ", ".join(headers) + ') VALUES ')
for values in csvFile:
    if values[0] != 'sym':
        values = ["'" + str(value) + "'" if i == 1 else str(value) for i, value in enumerate(values)]
        values = [value.replace("'s", "''s") for value in values]
        values = [value.replace("\v", "") for value in values]
        values = [value.replace("s' ", "s ") for value in values]
        outFile.write("(" + ", ".join(values) +"),\n")
openFile.close()
outFile.close()