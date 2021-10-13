import bpy
import csv

myfilepath = "C:\\Users\\pd1977\\Documents\\5. BlenderBIM\\ParameterMapping\\test.csv"

with open(myfilepath, newline="", mode='r', encoding='utf-8-sig') as csvfile:
    my_excel_file = csv.reader(csvfile, delimiter=";", quotechar='|')
    for row in my_excel_file:
        print(row)