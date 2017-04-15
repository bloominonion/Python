import calendar
import lxml.html
from lxml import etree
import random

import glob
import sys
import os
import fnmatch

import json
from pprint import pprint

def main():
    filePath = os.getcwd() + '\\Menus'

    options = []
    menus = []

    menuFiles = GetMenuFiles(filePath)
    for dataFile in menuFiles:
        print ("Opening menu: ", dataFile)
        with open(dataFile) as menu:    
            data = json.load(menu)
            for recipe in data:
                options.append(recipe)

    month = 4
    year = 2017
    lastChoice = ""
    for i in range(calendar.monthrange(year,month)[1]):
        count = 0
        while True:
            choice = random.choice(options)
            if choice != lastChoice:
                lastChoice = choice
                menus.append(choice)
                break
            count += 1
            if (count > 20):
                break

    cal = ProcessCal(month, year, menus)

    with open("test.html","w") as html:
        html.write(str(cal)) 


def PrintMenuDetails(jsonData):
    print("Recipe Name:", jsonData["recipeName"])
    print("Ingredients:")
    for ingredient in jsonData["ingredients"]:
        item = ingredient["item"]
        qty = ingredient["qty"]
        qtyType = ingredient["qty_type"]
        print ("{:>5} {:>6}\t{}".format(qty, qtyType, item))

def GetMenuFiles(path):
    menuFiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(path )
    for f in fnmatch.filter(files, '*.json')]
    return menuFiles


class ProcessCal():
    def __init__(self, month, year, menus):
        Cal = calendar.HTMLCalendar(calendar.SUNDAY)
        htmlCal = Cal.formatmonth(year,month)
        lxmlData = lxml.html.fromstring(htmlCal)
        self.html = lxml.html.tostring(lxmlData).decode("utf-8")
        self.etree = etree.fromstring(self.html)
        self.menus = menus
        self.hasRun = False

    def ProcessMonth(self):
        self.FixTable()
        self.SetMenus()
        self.hasRun = True

    def SetMenus(self):
        for elem in self.etree:
            for tr in elem:
                val = tr.text
                if val.isdigit():
                    newElem = etree.Element("button")
                    newElem.text = self.menus[int(val)-1]
                    tr.append(newElem)

    def FixTable(self):
        padding = b'3'
        # Fix table
        self.etree.set("border", '1')
        self.etree.set("cellspacing", padding)
        self.etree.set("cellpadding", padding)
        self.etree.set("style", 'width:%50')

    def CSSHead(self):
        string = """<!DOCTYPE html>
<html>
<head>
<style>
table, { 
    display: table;
    border-collapse: separate;
    border-spacing: 2px;
    border-color: gray;
    border: 1px solid black;
}
th, td {
   padding: 10px;
   text-align: right;
   border: 1px solid black;
   width: 100px;
}
td{
   height: 85px;
   font-weight: bold;
}
th{
   text-align: center;
}
button{
   width: 100%;
   height: 100%;
   border: none;
   background-color: white;
   text-align: left;
}
</style>
</head>
<body>"""
        return string

    def CSSTail(self):
        string = """
</body>
</html>"""
        return string

    def __str__(self):
        if not self.hasRun:
            self.ProcessMonth()
        htmlStr = lxml.html.tostring(self.etree, pretty_print=True).decode("utf-8")
        self.html = self.CSSHead() + htmlStr + self.CSSTail()
        return self.html


if __name__ == '__main__':
    main()