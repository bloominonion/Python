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
    outFile = "test.html"

    options = []
    menus = []

    recipes = RecipeHandler()
    menuFiles = GetMenuFiles(filePath)
    for dataFile in menuFiles:
        print ("Opening menu: ", dataFile)
        with open(dataFile) as menu:    
            data = json.load(menu)
            recipes.SetData(data)
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

    weekMgr = WeekMenuManager(month, year, menus)
    weeklyIngredients = []
    for weekMenu in weekMgr.GetWeeklyMenus():
        shopper = ShoppingList()
        for menu in weekMenu:
            for ing in recipes.GetIngredients(menu):
                shopper.AddIngredients(*ing)
            # recipes.PrintRecipeWithIngredients(menu,"   ")
        weeklyIngredients.append(shopper.IngredientList())

    cal = ProcessCal(month, year, menus, weeklyIngredients)
    with open(outFile,"w") as html:
        html.write(str(cal)) 

    # os.system('\"c:\program files (x86)\Google\Chrome\Application\chrome.exe\" ' + outFile)

def GetMenuFiles(path):
    menuFiles = [os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(path )
    for f in fnmatch.filter(files, '*.json')]
    return menuFiles

class ShoppingList():
    def __init__(self):
        self.accum = {}

    def AddIngredients(self,qty,qType,item):
        if item in self.accum.keys():
            if qType in self.accum[item].keys():
                val = self.accum[item][qType]
                self.accum[item][qType] = val + qty
            else:
                self.accum[item][qType] = qty
        else:
            self.accum[item] = { qType : qty }

    def IngredientList(self):
        result = []
        for ing in self.accum.keys():
            for qType in self.accum[ing].keys():
                result.append([ing, self.accum[ing][qType], qType])
        return result

    def PrintList(self):
        resultStr = ""
        for ing in self.accum.keys():
            resultStr += "{}:\n".format(ing)
            for qType in self.accum[ing].keys():
                resultStr += "   {} {}\n".format(self.accum[ing][qType], qType)
        return resultStr

class RecipeHandler():
    def __init__(self,data=None):
        if data is not None:
            self.data = data

    def SetData(self,data):
        self.data = data

    def PrintRecipeWithIngredients(self,recipe,indent=""):
        print(indent + self.data[recipe]["recipeName"])
        print(indent + "   Ingredients:")
        ingredients = self.GetIngredients(recipe)
        for ing in ingredients:
            print (indent + "      {:>5} {:>6}\t{}".format(ing[0], ing[1], ing[2]))

    def GetIngredients(self,recipe):
        ingredients = []
        for ingredient in self.data[recipe]["ingredients"]:
            item = ingredient["item"]
            qty = ingredient["qty"]
            qtyType = ingredient["qty_type"] 
            ingredients.append([float(qty),qtyType,item])
        return ingredients

class WeekMenuManager():
    def __init__(self, month, year, menus):
        self.month = month
        self.year = year
        self.menus = menus
        self.weekDaySets = []
        self.BuilWeekDaysList()

    def BuilWeekDaysList(self):
        numWeeks = calendar.Calendar(calendar.SUNDAY).itermonthdays2(self.year, self.month)
        weeklist = []
        for wk in numWeeks:
            if wk[0] > 0:
                weeklist.append(wk[0])
            if wk[1] == calendar.SATURDAY:
                self.weekDaySets.append(weeklist[:])
                del weeklist[:]

    def GetWeekDays(self,weekNum):
        return self.weekDaySets[weekNum]

    def GetWeeklyMenus(self):
        for week in self.weekDaySets:
            yield [self.menus[i-1] for i in week]

class ProcessCal():
    def __init__(self, month, year, menus, shopList):
        Cal = calendar.HTMLCalendar(calendar.SUNDAY)
        self.date = [month,year]
        htmlCal = Cal.formatmonth(year,month)
        lxmlData = lxml.html.fromstring(htmlCal)
        self.html = lxml.html.tostring(lxmlData).decode("utf-8")
        self.etree = etree.fromstring(self.html)
        self.menus = menus
        self.shopList = shopList
        self.hasRun = False

    def ProcessMonth(self):
        self.FixTable()
        self.SetMenus()
        self.AddShoppingList()
        self.hasRun = True

    def AddShoppingList(self):
        weekMgr = WeekMenuManager(self.date[0], self.date[1], self.menus)
        weekNum = 0

        table = etree.Element("table")
        table.set("class", b'shopList')
        tableRow = etree.Element("tr")
        for week in self.shopList:
            weekDays = weekMgr.GetWeekDays(weekNum)
            hdrStr = "Ingredients for " + calendar.month_abbr[self.date[0]] + " {}".format(weekDays[0])
            if len(weekDays) > 1:
                hdrStr += "-{}".format(weekDays[-1])

            if weekNum % 3 == 0:
                table.append(tableRow)
                tableRow = etree.Element("tr")

            head = etree.Element("th")
            head.text = hdrStr
            table.append(head)

            tableData = etree.Element("td")
            for ingredient in week:
                br = etree.Element("br")
                br.tail = "{}:{} {}".format(ingredient[0], ingredient[1], ingredient[2])
                tableData.append(br)
            tableRow.append(tableData)
            weekNum += 1
        table.append(tableRow)
        self.etree.append(table)

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
table { 
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
.shopList td {
   width: 300px;
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