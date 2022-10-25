from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import requests
import datetime

import pandas as pd

from PIL import Image
from PIL import Image, ImageFilter
import pytesseract
import time
import re
import cv2


class FirstNumCalculator:

    def __init__(self):
        self.numList = []
        self.gap1 = 0
        self.gap2 = 0
        self.gap3 = 0
        self.gapDict = {}
        self.gapKeyNumListValueDict = {}
        self.result = ""

    def setNumList(self, numList):
        print("FirstNumCalculator, numList => ", numList)
        self.numList = numList
        self.setGaps()
        self.setGapDicts()

    def add(self, x, y):
        return float(x) + float(y)

    def subtract(self, x, y):
        return float(x) - float(y)

    def subtractAndRound(self, x, y, d):
        return round(float(x) - float(y), d)

    def floatToString(self, floatNum):
        prevLen = len(str(floatNum).split('.')[0]) + 1
        return str(floatNum)[0:prevLen + 1]

    def sortDict(self, argDict):
        return dict(sorted(argDict.items(), key=lambda item: item[1]))

    def setGaps(self):
        self.gap1 = self.subtractAndRound(self.numList[0], self.numList[1], 1)
        self.gap2 = self.subtractAndRound(self.numList[1], self.numList[2], 1)
        self.gap3 = self.subtractAndRound(self.numList[2], self.numList[3], 1)
        print("=====================================================================================================")
        print("FIRST GAP => ", self.gap1, ", SCOND GAP => ", self.gap2, ", THIRD GAP => ", self.gap3)

    def setGapDicts(self):
        for i in range(1, len(self.numList) - 1):
            gap = self.subtractAndRound(self.numList[i], self.numList[i + 1], 1)
            self.gapDict[i] = gap
            if (self.gap1 > 0 and gap > 0) or (self.gap1 < 0 and gap < 0) or (self.gap1 == 0):
                similar = str(abs(self.subtractAndRound(self.gap1, gap, 1)))
                if similar in self.gapKeyNumListValueDict:
                    self.gapKeyNumListValueDict[similar].append(i)
                else:
                    self.gapKeyNumListValueDict[similar] = [i]
        print("=====================================================================================================")
        print("GAP DICT => ", self.gapDict)
        print("=====================================================================================================")
        print("GAP KEY NUM LIST VALUE DICT => ", self.gapKeyNumListValueDict)
        print("=====================================================================================================")


    def getFinalGap(self):
        tmpLi2 = []
        tmpLi3 = []

        for k in range(len(self.gapKeyNumListValueDict.keys())):
            curKey = str(k * 0.1)
            if curKey in self.gapKeyNumListValueDict:
                curList = self.gapKeyNumListValueDict[str(k * 0.1)]
                print("CUR KEY => ", curKey, ", CUR LIST => ", curList)
#             if curList:
                for num in curList:
                    if len(self.gapDict.keys()) >= int(num) + 1:
                        tmpLi2.append(self.gapDict[int(num) + 1])
                    if len(self.gapDict.keys()) >= int(num) + 2:
                        tmpLi3.append(self.gapDict[int(num) + 2])
                print("SECOND GAP LIST => ", tmpLi2)
                tmpLi22 = []
                tmpLi222 = []
                for gap in tmpLi2:
                    tmpLi22.append(abs(self.gap2 - gap))
                print("SECOND GAP LIST CALCULATED => ", tmpLi22)
                for i, gap in enumerate(tmpLi22):
                    if min(tmpLi22) == gap:
                        tmpLi222.append(curList[i])
                print("SECOND NUMBER LIST => ", tmpLi222)
                if len(tmpLi222) > 0:
                    print("THIRD GAP LIST => ", tmpLi3)
                    tmpLi33 = []
                    for gap in tmpLi3:
                        tmpLi33.append(abs(self.gap3 - gap))
                    print("THIRD GAP LIST CALCULATED => ", tmpLi33)
                    val = 10000
                    number = 0
                    for i in tmpLi222:
                        idx = curList.index(i)
                        if len(tmpLi33) >= idx:
                            if val > tmpLi33[idx]:
                                val = tmpLi33[idx]
                                number = idx
                    finalNumber = curList[number]
                    print("POINTS => (", self.numList[finalNumber - 1], ",", self.numList[finalNumber],")")
                    return self.subtractAndRound(self.numList[finalNumber - 1], self.numList[finalNumber], 4)
                else:
                    return 0
#                     finalNumber = tmpLi222[0]
#                     print("POINTS => (", self.numList[finalNumber -1], ",", self.numList[finalNumber],")")
#                     return self.subtractAndRound(self.numList[finalNumber -1], self.numList[finalNumber], 4)

    def execute(self, numList):
        self.setNumList(numList)
        finalGap = self.getFinalGap()
        print("FINAL GAP => ", finalGap)
        print("FIRST NUM => ", self.numList[0])
        tmpResult = str(self.add(self.numList[0], finalGap))
        print("TMP RESULT => ", tmpResult)
        self.result = tmpResult.split('.')[0] + '.' + tmpResult.split('.')[1][0]
        print("=====================================================================================================")
        print("RESULT => ", self.result)
        print("=====================================================================================================")


class SecondNumCalculator:

    def __init__(self):
        self.numList = []
        self.result = ""
        self.numListSize = 0

    def setNumList(self, numList):
        print("SecondNumCalculator, numList => ", numList)
        self.numList = numList
        self.numListSize = len(self.numList)

    def convertToNumList(self):
        tmpNumList = []
        for numStr in self.numList:
            tmpNumList.append(int(numStr))
        return tmpNumList

    def getMaxIdxList(self, numList):
        maxNum = max(numList)
        maxIdxList = []
        for idx, num in enumerate(numList):
            if maxNum == num:
                maxIdxList.append(idx)
        return maxIdxList

    def pickPastNumDict(self, idxList, past):
        numDict = {}
        for idx in idxList:
            pastIdx = idx - past
            if pastIdx < 0:
                pastIdx += self.numListSize
            elif pastIdx >= self.numListSize:
                pastIdx -= self.numListSize
            tmpNum = int(self.numList[pastIdx])
            numDict[idx] = tmpNum
        return numDict

    def findSecondNumber(self, maxNumIdxList):
        maxNumIdxListSize = len(maxNumIdxList)
        if maxNumIdxListSize > 1:
            if maxNumIdxListSize == self.numListSize:
                return '9'

            for i in range(self.numListSize - 1):
                pastNumDict = self.pickPastNumDict(maxNumIdxList, i)
                pastNumList = list(pastNumDict.values())
                pastMaxIdxList = self.getMaxIdxList(pastNumList)
                if len(pastMaxIdxList) == 1:
                    pastMaxIdx = pastMaxIdxList[0]
                    return str(list(pastNumDict.keys())[pastMaxIdx])
        else:
            return str(maxNumIdxList[0])

    def execute(self, numList):
        self.setNumList(numList)
        if len(self.numList) > 0:
            maxNumIdxList = self.getMaxIdxList(self.convertToNumList())
            self.result = self.findSecondNumber(maxNumIdxList)

class LastNumCalculatorCase12:

    def __init__(self):
        self.numList = []
        self.result = ""

    def setNumList(self, numList):
        print("LastNumCalculatorCase12, numList => ", numList)
        self.numList = numList

    def reverseSortDictByValue(self, argDict):
        return dict(reversed(sorted(argDict.items(), key=lambda item: item[1])))

    def reverseSortDictByKey(self, argDict):
        return dict(sorted(argDict.items(), key = lambda item: item[0], reverse = True))

    def getFirstKeyByDict(self, argDict):
        if len(list(argDict.keys())) > 0:
            return list(argDict.keys())[0]
        else:
            return ''

    def duplicatedValuesCheck(self, argDict):
        return len(list(set(argDict.values()))) == 1

    def initThirdCountDictByList(self):
        countDict = {}
        for num in self.numList:
            if num:
                key = num.split(".")[1][2]
                countDict[key] = 0
        return countDict

    def initFourthCountDictByList(self):
        countDict = {}
        for num in self.numList:
            if num:
                key = num.split(".")[1][3]
                countDict[key] = 0
        return countDict

    def getThirdNumber(self):
        countDict = self.initThirdCountDictByList()
        for num in self.numList:
            if num:
                key = num.split(".")[1][2]
                countDict[key] = 0
                countDict[key] += 1
        resultDict = {}
        if self.duplicatedValuesCheck(countDict):
            resultDict = self.reverseSortDictByKey(countDict)
        else:
            resultDict = self.reverseSortDictByValue(countDict)
        return self.getFirstKeyByDict(resultDict)

    def getFourthNumber(self):
        countDict = self.initFourthCountDictByList()
        for num in self.numList:
            if num:
                key = num.split(".")[1][3]
                countDict[key] = 0
                countDict[key] += 1
        if self.duplicatedValuesCheck(countDict):
            resultDict = self.reverseSortDictByKey(countDict)
        else:
            resultDict = self.reverseSortDictByValue(countDict)
        return self.getFirstKeyByDict(resultDict)

    def execute(self, numList):
        self.setNumList(numList)
        print("CALCULATE THIRD AND FOURTH NUMBER ...")
        thirdNumber = self.getThirdNumber()
        print("THIRD NUMBER => ", thirdNumber)
        fourthNumber = self.getFourthNumber()
        print("FOURTH NUMBER => ", fourthNumber)
        self.result = thirdNumber + fourthNumber

class LastNumCalculatorCase3:

    def __init__(self):
        self.numList1 = []
        self.numList2 = []
        self.result = ""

    def setNumList(self, numList1, numList2):
        print("LastNumCalculatorCase3, numList1 => ", numList1, ", numList2 => ", numList2)
        self.numList1 = numList1
        self.numList2 = numList2

    def subtractAndRound(self, x, y):
        return round(float(x) - float(y), 4)

    def getThirdAndFourthNumber(self, numberStr):
        numStr = numberStr.split(".")[1]
        if len(numStr) > 3:
            return numStr[2] + numStr[3]
        else:
            if len(numStr) == 3:
                return numStr[2] + "0"
            else:
                return "00"

    def execute(self, numList):
        self.setNumList(numList[0], numList[1])
        if len(self.numList1) > 0 and len(self.numList2) > 0:
            print("CALCULATE THIRD AND FOURTH NUMBER ...")
            x = max(self.numList2)
            subList = []
            subList.append(self.subtractAndRound(self.numList1[0], x))

            for i in range(1, len(self.numList1)):
                subList.append(self.subtractAndRound(self.numList1[i], self.numList1[i - 1]))

            lastNumber = self.numList1[subList.index(max(subList))]
            print("LAST NUMBER => ", lastNumber)
            print("LAST NUMBER CALCULATED -> ", self.subtractAndRound(lastNumber, '0.0001'))
            self.result = self.getThirdAndFourthNumber(str(self.subtractAndRound(lastNumber, '0.0001')))
        elif len(self.numList1) > 0:
            self.result = self.getThirdAndFourthNumber(str(self.subtractAndRound(min(self.numList1), '0.0001')))

class NumCalculator:

    def __init__(self, case):
        print("* INIT NUMBER CALCULATOR CASE : ", case)
        self.firstNumCalculator = FirstNumCalculator()
        self.secondNumCalculator = SecondNumCalculator()
        if case == 3:
            self.lastNumCalculator = LastNumCalculatorCase3()
        else:
            self.lastNumCalculator = LastNumCalculatorCase12()

    def getFirstSecondNum(self, numList1, numList2):
        self.firstNumCalculator.execute(numList1)
        self.secondNumCalculator.execute(numList2)
        return self.firstNumCalculator.result + self.secondNumCalculator.result

    def getResultNumCase(self, numList3):
        self.lastNumCalculator.execute(numList3)
        return self.lastNumCalculator.result

class BribidBackOffice:

    def __init__(self, id, pw, startDt, endDt):
        self.id = id
        self.pw = pw
        self.startDt = startDt
        self.endDt = endDt
        print("START DT => ", startDt, ", END DT => ", endDt)
        self.mainUrl = "http://www.brbid.co.kr/Back_Office/admin_main.html"
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.authorized = False
        self.gongoList = []
        self.gongoNameList = []
        self.gongoNumberDict1 = {}
        self.gongoNumberDict2 = {}
        self.gongoNumberDict3 = {}

    def verifyCaptcha(self, element, path):
        location = element.location
        size = element.size
        self.driver.save_screenshot(path)
        image = Image.open(path)

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        image = image.crop((left, top, right, bottom))
        image.save(path, 'png')

        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
        numbersString = pytesseract.image_to_string(image, config=custom_config)
        numbersInt = re.sub(r'[a-z\n]', '', numbersString.lower())
        self.driver.find_element(By.NAME, "wr_key").send_keys(numbersInt)

    def login(self):
        #pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pytesseract.pytesseract.tesseract_cmd =r"/usr/local/Cellar/tesseract/5.2.0/bin/tesseract"
        self.driver.implicitly_wait(5)
        self.driver.get(self.mainUrl)
        time.sleep(3)

        self.driver.find_element(By.NAME, "admin_ID").send_keys(self.id)
        self.driver.find_element(By.NAME, "admin_PW").send_keys(self.pw)
        self.driver.find_element(By.NAME, "save_ID").click()


        while not self.authorized:
            img = self.driver.find_element(By.ID, "kcaptcha_image")
            img.click()
            self.verifyCaptcha(img, "captcha.png")
            self.driver.find_element(By.CLASS_NAME, "btn_login").click()
            try:
                alert = self.driver.switch_to.alert
                if alert:
                    alert.accept()
                else:
                    self.authorized = True
                    time.sleep(3)
            except:
                print("LOGIN COMPLETED...")
                break

    def openPage(self, pageUrl):
        print("OPEN PAGE...", pageUrl)
        self.driver.implicitly_wait(5)
        self.driver.get(pageUrl)
        time.sleep(5)

    def setGongGoList(self):
        self.driver.implicitly_wait(5)
        time.sleep(5)
        tblBoardList = self.driver.find_element(By.CLASS_NAME, 'tbl_board_list')
        aList = tblBoardList.find_elements(By.TAG_NAME, 'a')
        for a in aList:
            if a.get_attribute("onclick"):
                self.gongoList.append(a)
        print("* GONGGO LIST COUNT : ", len(self.gongoList))

    def clickAnalysisProgramBtn(self):
        h4 = self.driver.find_element(By.TAG_NAME, 'h4')
        spanList = h4.find_elements(By.TAG_NAME, 'span')
        aList = spanList[1].find_elements(By.TAG_NAME, 'a')
        analysisProgramBtn = aList[0]
        analysisProgramBtn.click()

    def getFirstCaseTotalNum(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element(By.XPATH, "//input[@value='12개월']").click()
        self.driver.find_element(By.XPATH, "//input[@value='검색']").click()
        totalNum = self.driver.find_element(By.ID, 'TotalNum').text
        return int(totalNum)

    def getSecondCaseTotalNum(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        gongsaAll = self.driver.find_element(By.XPATH, '//span[text()="[공사전체]"]')
        if gongsaAll.text:
            gongsaAll.click()
        else:
            gumaAll = self.driver.find_element(By.XPATH, '//span[text()="[구매전체]"]')
            if gumaAll.text:
                gumaAll.click()
            else:
                self.driver.find_element(By.XPATH, '//span[text()="[용역전체]"]').click()
        self.driver.find_element(By.ID, 'A000000').click()
        self.driver.find_element(By.XPATH, "//input[@value='12개월']").click()
        self.driver.find_element(By.XPATH, "//input[@value='검색']").click()
        alert = self.driver.switch_to.alert
        alert.accept()
        total_num = self.driver.find_element(By.ID, 'TotalNum').text
        return int(total_num)

    def getThirdCaseTotalNum1(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element(By.NAME, "OrderName").clear()
        self.driver.find_elements(By.XPATH, "//input[@value='AND']")[0].click()
        self.driver.find_elements(By.XPATH, "//input[@value='AND']")[1].click()
        self.driver.find_element(By.XPATH, "//input[@value='12개월']").click()
        self.driver.find_element(By.XPATH, "//input[@value='검색']").click()
        total_num = self.driver.find_element(By.ID, 'TotalNum').text
        return int(total_num)

    def getThirdCaseTotalNum2(self):
        self.driver.find_elements(By.XPATH, "//input[@value='OR']")[0].click()
        self.driver.find_elements(By.XPATH, "//input[@value='OR']")[1].click()
        self.driver.find_element(By.XPATH, "//input[@value='12개월']").click()
        self.driver.find_element(By.XPATH, "//input[@value='검색']").click()
        total_num = self.driver.find_element(By.ID, 'TotalNum').text
        return int(total_num)

    def removeEmptyStringInList(self, argList):
        while("" in argList):
            argList.remove("")
        return argList

    def getFirstNumList(self):
        numList = []
        for td in self.driver.find_elements(By.XPATH, '//td//font'):
            numStr = td.text
            if len(numStr) > 2:
                numList.append(td.text)
        return self.removeEmptyStringInList(numList)

    def getSecondNumList(self):
        numList = []
        table = self.driver.find_elements(By.ID, 'TableXY')[0]
        trList = table.find_elements(By.TAG_NAME, 'tr')
        strongList = trList[len(trList) - 1].find_elements(By.TAG_NAME, 'strong')
        for strong in strongList:
            numList.append(strong.text)
        return numList

    def getThirdNumListCase3(self, searchNumber):
        self.clickFirstGongo()
        self.clickDistributionTable()

        tableXY = self.driver.find_elements(By.ID, 'TableXY')[0]
        tableXYtrList = tableXY.find_elements(By.TAG_NAME, 'tr')

        completed = False
        numList1 = []
        numList2 = []

        for idx, tr in enumerate(tableXYtrList):
            if idx > 2 and idx < len(tableXYtrList) - 3:
                if completed:
                    break
                tdList = tr.find_elements(By.TAG_NAME, 'td')
                for td in tdList:
                    if completed:
                        break
                    if td.get_attribute("onclick"):
                        jsContent = td.get_attribute("onclick")
                        if str(float(searchNumber) - 0.01) in jsContent:
                            if td.text.strip():
                                td.click()
                                time.sleep(3)
                                self.driver.switch_to.window(self.driver.window_handles[2])
                                txtRedList = self.driver.find_elements(By.CLASS_NAME, 'txt_red')
                                for txtRed in txtRedList:
                                    numList2.append(txtRed.text)
                                self.driver.close()
                                self.driver.switch_to.window(self.driver.window_handles[1])
                        if searchNumber in jsContent:
                            if td.text.strip():
                                td.click()
                                time.sleep(3)
                                self.driver.switch_to.window(self.driver.window_handles[2])
                                txtRedList = self.driver.find_elements(By.CLASS_NAME, 'txt_red')
                                for txtRed in txtRedList:
                                    numList1.append(txtRed.text)
                                self.driver.close()
                            completed = True
                            break
        numList = [numList1, numList2]
        return numList

    def clickFirstGongo(self):
        tblBoardList = self.driver.find_element(By.CLASS_NAME, 'tbl_board_list')
        tblBoardTrList = tblBoardList.find_elements(By.TAG_NAME, 'tr')
        tblBoardTrList[1].find_element(By.TAG_NAME, 'input').click()
        time.sleep(3)

    def clickDistributionTable(self):
        buTitList = self.driver.find_element(By.CLASS_NAME, 'bu_tit')
        liList = buTitList.find_elements(By.XPATH, '//ul//li')
        distBtn = liList[1]
        distBtn.click()

    def subtractAndRound(self, x, y):
        return round(float(x) - float(y), 4)

    def getThirdNumListCase12(self, searchNumber):
        time.sleep(3)
        numList = []
        resultId = 'N' + searchNumber.replace('.', '')
        try:
            divTitle = self.driver.find_element(By.ID, resultId).find_element(By.TAG_NAME, 'div').get_attribute('title')
            if divTitle:
                numList = divTitle.replace('\n', '').split('%')
        except NoSuchElementException:
            try:
                divTitle = self.driver.switch_to.frame(self.driver.find_element(By.ID, resultId).find_element(By.TAG_NAME, 'div').get_attribute('title'))
                if divTitle:
                    numList = divTitle.replace('\n', '').split('%')
            except NoSuchElementException:
                print("NO SUCH ELEMENT...")
        return numList

    def calResultNumByCase(self, case):
        numCalculator = NumCalculator(case)
        firstNumList = self.getFirstNumList()
        secondNumList = self.getSecondNumList()
        searchNum = numCalculator.getFirstSecondNum(firstNumList, secondNumList)
        print("FirstNumber + SecondNumber => ", searchNum)
        if case == 3:
            thirdNumList = self.getThirdNumListCase3(searchNum)
        else:
            thirdNumList = self.getThirdNumListCase12(searchNum)
        resultNum = numCalculator.getResultNumCase(thirdNumList)
        if not resultNum:
            print("=====================================================================================================")
            print("** RESULT NUMBER => ", searchNum + "99")
            print("=====================================================================================================")
            return searchNum + "99"
        else :
            print("=====================================================================================================")
            print("** RESULT NUMBER => ", searchNum + resultNum)
            print("=====================================================================================================")
            return searchNum + resultNum

    def closeAnalysisProgram(self):
        time.sleep(3)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.close()
        time.sleep(3)

    def searchFirstCaseNumber(self, gongoName):
        self.clickAnalysisProgramBtn()
        totalNum = self.getFirstCaseTotalNum()
        print("* FIRST CASE TOTAL NUM :", totalNum)
        if totalNum >= 30:
            print("START FIRST CASE PROCESS...")
            self.gongoNumberDict1[gongoName] = self.calResultNumByCase(1)
        else:
            print("NOT ENOUGH DATA...")
        self.closeAnalysisProgram()

    def searchSecondCaseNumber(self, gongoName):
        self.clickAnalysisProgramBtn()
        totalNum = self.getSecondCaseTotalNum()
        print("* SECOND CASE TOTAL NUM :", totalNum)
        if totalNum >= 30:
            print("START SECOND CASE PROCESS...")
            self.gongoNumberDict2[gongoName] = self.calResultNumByCase(2)
        else:
            print("NOT ENOUGH DATA...")
        self.closeAnalysisProgram()

    def searchThirdCaseNumber(self, gongoName):
        self.clickAnalysisProgramBtn()
        totalNum = self.getThirdCaseTotalNum1()
        print("* THIRD CASE TOTAL NUM (CONDITION : AND) :", totalNum)
        if totalNum >= 30:
            print("START THIRD CASE PROCESS...")
            self.gongoNumberDict3[gongoName] = self.calResultNumByCase(3)
        else:
            totalNum = self.getThirdCaseTotalNum2()
            print("* THIRD CASE TOTAL NUM (CONDITION : OR):", totalNum)
            print("START THIRD CASE PROCESS...")
            if totalNum >= 30:
                self.gongoNumberDict3[gongoName] = self.calResultNumByCase(3)
                print("NOT ENOUGH DATA...")
        self.closeAnalysisProgram()

    def clickGongo(self, gongo):
        gongo.click()
        time.sleep(3)

    def searchNumberProcess(self, i):
        gongo = self.clickGongoFromList(i)
        gongoName = gongo.text
        print("* GONGO NAME : ", gongoName)
        self.gongoNameList.append(gongoName)
        self.clickGongo(gongo)
        self.searchFirstCaseNumber(gongoName)
        gongo = self.clickGongoFromList(i)
        self.clickGongo(gongo)
        self.searchSecondCaseNumber(gongoName)
        gongo = self.clickGongoFromList(i)
        self.clickGongo(gongo)
        self.searchThirdCaseNumber(gongoName)

    def clickGongoFromList(self, i):
        self.driver.switch_to.window(self.driver.window_handles[0])
        tblBoardList = self.driver.find_element(By.CLASS_NAME, 'tbl_board_list')
        trListTmp = tblBoardList.find_elements(By.TAG_NAME, 'tr')

        trList = []
        for tr in trListTmp:
            if tr.get_attribute('bgcolor'):
                trList.append(tr)

        tr = trList[i]
        tdList = tr.find_elements(By.TAG_NAME, 'td')
        gongo = tdList[3]
        return gongo

    def clickGongoList(self):
        for i in range(len(self.gongoList)):
            print("SEARCH NUMBER PROCESS...")
            self.searchNumberProcess(i)

    def run(self):
        print("START PROGRAM...")
        self.login()
        pageUrl = "http://www.brbid.co.kr/Back_Office/test.html?rdoFindDate=FinishDTime&txtSDate=" + self.startDt + "&txtEDate=" + self.endDt + "&lstMasterID=" + self.id + "&txtKind="
        self.openPage(pageUrl)
        self.setGongGoList()
        self.clickGongoList()

class ExcelManager:
    def __init__(self, dict1, dict2, dict3):
        self.dictList = [dict1, dict2, dict3]
        self.dict1 = dict1
        self.dict2 = dict2
        self.dict3 = dict3

    def convertCsvFile(self, dict, i):
        columns = ['공고명', '업체 예가']
        df = pd.DataFrame(columns=columns)
        col = df.columns

        for title, content in dict.items():
            tmp_row = []
            tmp_row.append(title)
            tmp_row.append(content)
            df_row = pd.Series(tmp_row, index=col)
            df = df.append(df_row, ignore_index=True)

        df.to_csv("./RES_GONGO_NUMBER_CASE_" + str(i) + ".csv", index=False, encoding="utf-8-sig")

    def downloadCsvFiles(self):
        for i, dict in enumerate(self.dictList):
            self.convertCsvFile(dict, i)
            print(">> DOWNLOAD FILE COMPLETED : ./RES_GONGO_NUMBER_CASE_" + str(i) + ".csv")

def main():
    id = input(">> Enter Id :").strip()
    if not id:
        id = 'xxxxxxxx'
    pw = input(">> Enter Password :").strip()
    if not pw:
        pw = 00000000
    startDt = input(">> Enter Start Ddate (ex, 2022-10-19) :").strip()
    if not startDt:
        startDt = datetime.date.today().strftime("%Y-%m-%d")
    endDt = input(">> Enter End Date (ex, 2022-10-21) :").strip()
    if not endDt:
        twoDaysLater = datetime.date.today() + datetime.timedelta(days=2)
        endDt = twoDaysLater.strftime("%Y-%m-%d")

    bbo = BribidBackOffice(id, pw, startDt, endDt)
    bbo.run()

    em = ExcelManager(bbo.gongoNumberDict1, bbo.gongoNumberDict2, bbo.gongoNumberDict3)
    em.downloadCsvFiles()

if __name__ == "__main__":
    main()
# main()