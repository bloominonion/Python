from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import platform
import time
import sys
import os

def main():
    import Authorization
    with WebInterface(user=Authorization.GetUser(), password=Authorization.GetPassword()) as con:
        con.LogDiaper("dirty and wet")
        sess = Nursing(0,500,500)
        con.LogNursing(sess)
##    import time
##    from pprint import pprint
##    testNurse = Nursing(1)
##    time.sleep(3)
##    testNurse.Switch()
##    time.sleep(1)
##    pprint(testNurse.GetTimes())

class WebInterface(object):
    url = r"https://www.baby-connect.com/home"

    ids = { 
        "bm" : "diaper1", 
        "bmwet" : "diaper2",
        "wet" : "diaper3",
        "dry" : "diaper4"
    }

    def __init__(self, user, password):
        self.user = user
        self.password = password

        if platform.system() == 'Linux':
            self.driver = webdriver.Firefox()
        else:
            self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        elem = self.driver.find_element_by_name("email")
        elem.clear()
        elem.send_keys(user)
        elem = self.driver.find_element_by_name("pass")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        timeCycles = 0
        timeWait = 2
        while "logout" not in self.driver.page_source:
            if timeCycles > 5:
                break
            time.sleep(timeWait)
            timeCycles += 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.close()
        
    def __del__(self):
        print ("Finalizing session")
        print (self.driver.close())

    def LogDiaper(self, logType):
        logType = str(logType)
        print ("Diaper log:", logType)
        isDirty = bool('poopy' in logType
                    or 'dirty' in logType
                    or 'poop' in logType)

        isWet = bool('wet' in logType)

        diaperType = None
        if isDirty and isWet:
            diaperType = "bmwet"
        elif isDirty and not isWet:
            diaperType = "bm"
        else:
            diaperType = "wet"

        # Fire pop-up box for logging
        self.driver.find_element_by_partial_link_text("Diaper").click()
        time.sleep(1)

        # Set type of diaper and log it.
        self.driver.find_element_by_id(self.ids[diaperType]).click()
        self.driver.find_element_by_css_selector(".ui-button-text-only .ui-button-text").click()
        # print ("Diaper logged...")

    def LogNursing(self, nursing):
        data = nursing.GetTimes()
        self.driver.find_element_by_partial_link_text("Nursing").click()
        time.sleep(1)
        elem = self.driver.find_element_by_id("timeinput")
        elem.clear()
        elem.send_keys(data['start'])
        elem = self.driver.find_element_by_id("endtimeinput")
        elem.clear()
        elem.send_keys(data['end'])
        duration = data['left'] + data['right']
        durM = 0
        durH = 0
        if duration > 60:
            durM = duration % 60
            durH = (duration-durM)/60
        else:
            durM = duration
        elem = self.driver.find_element_by_id("hduration")
        elem.clear()
        elem.send_keys(str(durH))
        elem = self.driver.find_element_by_id("mduration")
        elem.clear()
        elem.send_keys(str(durM))
        elem = self.driver.find_element_by_id("left_side")
        elem.clear()
        elem.send_keys(str(data['left']))
        elem = self.driver.find_element_by_id("right_side")
        elem.clear()
        elem.send_keys(str(data['right']))

        if data["last"] == 1:
            self.driver.find_element_by_id("last_left").click()
        else:
            self.driver.find_element_by_id("last_right").click()

        self.driver.find_element_by_css_selector(".ui-button-text-only .ui-button-text").click()
        print ("Nursing session logged...")

# Class for handling the time tracking of a nursing session.
# This has the utilities to stop/start a session ans switch sides
class Nursing(object):
    def __init__(self, side, timeL=None, timeR=None):
        self.timeBegin = datetime.now() if timeL is None else datetime.now() - timedelta(seconds=(timeL+timeR))
        self.timeStart = datetime.now()
        self.side = side  # 0 = L, 1 = R
        self.durL = 0 if timeL is None else timeL
        self.durR = 0 if timeR is None else timeR

    def Switch(self):
        self.AddTime()
        self.side = 0 if self.side else 1

    def Pause(self):
        self.AddTime()
        self.timeStart = None

    def Resume(self):
        self.timeStart = datetime.now()

    def AddTime(self):
        now = datetime.now()
        if self.timeStart is not None:
            if self.side:
                self.durR += (now - self.timeStart).total_seconds()
            else:
                self.durL += (now - self.timeStart).total_seconds()
        self.timeStart = now

    def GetTimes(self):
        self.AddTime()
        return {
            "start":self.timeBegin.strftime("%I:%M%p"), 
            "left":round((self.durL/60), 0), 
            "right":round((self.durR/60), 0),
            "end":datetime.now().strftime("%I:%M%p"),
            "last":self.side
        }

if __name__ == '__main__':
    main()
