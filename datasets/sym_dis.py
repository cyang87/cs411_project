import csv
import sys

openFile = open('sym_dis.csv', 'r')
csvFile = csv.reader(openFile)
diseases = next(csvFile)
headers = ['DiseaseID', 'SymptomID', 'Weight']
outFile = open('sym_dis.sql', 'w')

outFile.write(
    'CREATE TABLE sym_dis (' + headers[0] + ' INTEGER NOT NULL, ' + headers[1] + ' INTEGER NOT NULL, ' + headers[2] + ' INTEGER NOT NULL);\n')

outFile.write('INSERT INTO sym_dis (' + ", ".join(headers) + ') VALUES ')
for i, values in enumerate(csvFile):
    for j, value in enumerate(values):
        value = float(value)
        if j > 0 and value != 0.0:
            enter_values = [int(float(diseases[j])), int(float(values[0])), int(value)]
            enter_values = [str(val) for val in enter_values]
            outFile.write("(" + ", ".join(enter_values) +"),\n")
openFile.close()
outFile.close()