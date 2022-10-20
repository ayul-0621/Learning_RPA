from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
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
        self.result = ""
        
    def setNumList(self, numList):
        self.numList = numList
        
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

    def findPointByIndex(self, idx):
        x = self.numList[idx]
        y = self.numList[idx + 1]
        gap = self.subtractAndRound(x, y, 1)
        gapDict = {}
        for i in range(idx + 1, len(self.numList) - 1):
            tmpGap = self.subtractAndRound(self.numList[i], self.numList[i + 1], 1)
            if (gap > 0 and tmpGap > 0) or (gap < 0 and tmpGap < 0) or (gap == tmpGap):
                gapDict[i] = abs(self.subtractAndRound(gap, tmpGap, 1))
        return self.sortDict(gapDict)

    def findStartIndex(self):
        firstDict = self.findPointByIndex(0)
        secondDict = self.findPointByIndex(1)
        for k1, v1 in firstDict.items():
            for k2, v2 in secondDict.items():
                if k1 + 1 == k2:
                    return k1 

    def execute(self, numList):
        self.setNumList(numList)
        startIndex = self.findStartIndex()
        prevStartIndex = startIndex - 1
        nexGap = self.subtractAndRound(self.numList[prevStartIndex], self.numList[startIndex], 4)
        nextNumber = self.add(self.numList[0], nexGap)
        self.result = self.floatToString(nextNumber)

class SecondNumCalculator:
    
    def __init__(self):
        self.numList = []
        self.result = ""
    
    def setNumList(self, numList):
        self.numList = numList

    def reverseSortDict(self, argDict):
        return dict(reversed(sorted(argDict.items(), key=lambda item: item[1])))

    def getMinValueFromDict(self, argDict):
        return min(list(argDict.values()))

    def createIdxDictByList(self):
        idxDict = {}
        for i, num in enumerate(self.numList):
            idxDict[i] = num
        return self.reverseSortDict(idxDict)

    def createIdxListByDict(self, idxDict):
        idxList = []
        maxNum = 0
        i = 0
        for k, v in self.reverseSortDict(idxDict).items():
            if i == 0:
                maxNum = v
            if maxNum <= v:
                idxList.append(k)
            i += 1
        return idxList

    def findMaxIdxByListAndDict(self, idxList, idxDict):
        curPrevMax = self.getMinValueFromDict(idxDict)
        maxIdx = 0
        for i in idxList:
            if i == 0:
                prev = len(idxList)
            else:
                prev = i - 1
            if curPrevMax < idxDict[prev]:
                curPrevMax = idxDict[prev]
                maxIdx = i
        return maxIdx

    def execute(self, numList):
        self.setNumList(numList)
        if len(self.numList1) > 0:
            idxDict = self.createIdxDictByList()
            idxList = self.createIdxListByDict(idxDict)
            self.result = str(self.findMaxIdxByListAndDict(idxList, idxDict))
    
class LastNumCalculatorCase12:
    
    def __init__(self):
        self.numList = []
        self.result = ""
    
    def setNumList(self, numList):
        self.numList = numList
        
    def reverseSortDictByValue(self, argDict):
        return dict(reversed(sorted(argDict.items(), key=lambda item: item[1])))
    
    def reverseSortDictByKey(self, argDict):
        return dict(sorted(argDict.items(), key = lambda item: item[0], reverse = True))

    def getFirstKeyByDict(self, argDict):
        if len(list(argDict.keys())) > 0:
            return list(argDict.keys())[0]
        else:
            return '0'
    
    def duplicatedValuesCheck(self, argDict):
        return len(list(set(argDict.values()))) == 1
        
    def initThirdCountDictByList(self):
        countDict = {}
        for num in self.numList:
            key = num[6]
            countDict[key] = 0
        return countDict
    
    def initFourthCountDictByList(self):
        countDict = {}
        for num in self.numList:
            key = num[7]
            countDict[key] = 0
        return countDict
        
    def getThirdNumber(self):
        countDict = self.initThirdCountDictByList()
        for num in self.numList:
            key = num[6]
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
            key = num[7]
            countDict[key] += 1
        if self.duplicatedValuesCheck(countDict):
            resultDict = self.reverseSortDictByKey(countDict)
        else:
            resultDict = self.reverseSortDictByValue(countDict)
        return self.getFirstKeyByDict(resultDict)
        
    def execute(self, numList):
        self.setNumList(numList)
        thirdNumber = self.getThirdNumber()
        fourthNumber = self.getFourthNumber()
        self.result = thirdNumber + fourthNumber

class LastNumCalculatorCase3:
    
    def __init__(self):
        self.numList1 = []
        self.numList2 = []
        self.result = ""
    
    def setNumList(self, numList1, numList2):
        self.numList1 = numList1
        self.numList2 = numList2
        
    def subtractAndRound(self, x, y):
        return round(float(x) - float(y), 4)

    def execute(self, numList):
        self.setNumList(numList[0], numList[1])
        if len(self.numList1) > 0 and len(self.numList2) > 0:
            x = max(self.numList2)
            subList = []
            subList.append(self.subtractAndRound(self.numList1[0], x))

            for i in range(1, len(self.numList1)):
                subList.append(self.subtractAndRound(self.numList1[i], self.numList1[i - 1]))

            lastNumber = self.numList1[subList.index(max(subList))]
            self.result = str(self.subtractAndRound(lastNumber, '0.0001'))

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
        self.mainUrl = "http://www.brbid.co.kr/Back_Office/admin_main.html?lid=9421&lip=121.171.87.234"
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
        pytesseract.pytesseract.tesseract_cmd = r"/usr/local/Cellar/tesseract/5.2.0/bin/tesseract"
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
            self.driver.find_element(By.XPATH, '//span[text()="[구매전체]"]').click()
        self.driver.find_element(By.ID, 'A000000').click()
        self.driver.find_element(By.XPATH, "//input[@value='12개월']").click()
        self.driver.find_element(By.XPATH, "//input[@value='검색']").click()
        alert = self.driver.switch_to.alert
        alert.accept()
        total_num = self.driver.find_element(By.ID, 'TotalNum').text
        return int(total_num)

    def getThirdCaseTotalNum(self):
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element(By.NAME, "OrderName").clear()
        self.driver.find_elements(By.XPATH, "//input[@value='AND']")[0].click()
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
    
    def getThirdNumListCase12(self, searchNumber):
        tableXY = self.driver.find_elements(By.ID, 'TableXY')[0]
        tableXYtrList = tableXY.find_elements(By.TAG_NAME, 'tr')

        completed = False
        numList = []

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
                        if searchNumber in jsContent:                           
                            if td.text.strip():
                                td.click()
                                time.sleep(3)
                                self.driver.switch_to.window(self.driver.window_handles[2])
                                txtRedList = self.driver.find_elements(By.CLASS_NAME, 'txt_red')
                                for txtRed in txtRedList:
                                    numList.append(txtRed.text)
                                self.driver.close()
                            completed = True
                            break
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

    def getThirdNumListCase3(self, searchNumber):
        self.clickFirstGongo()
        self.clickDistributionTable()
        resultId = 'N' + searchNumber.replace('.', '')
        divTitle = self.driver.find_element(By.ID, resultId).find_element(By.TAG_NAME, 'div').get_attribute('title')
        numList = []
        numList1 = []
        numList2 = []
        if divTitle:
            numList1 = divTitle.replace('\n', '').split('%')
            prevResultId = 'N' + self.subtractAndRound(float(searchNumber), 0.0001).replace('.', '')
            prevDivTitle = self.driver.find_element(By.ID, prevResultId).find_element(By.TAG_NAME, 'div').get_attribute('title')
            numList2 = prevDivTitle.replace('\n', '').split('%')
        numList.append(numList1)
        numList.append(numList2)
        return numList
    
    def calResultNumByCase(self, case):
        numCalculator = NumCalculator(case)
        firstNumList = self.getFirstNumList()
        secondNumList = self.getSecondNumList()
        searchNum = numCalculator.getFirstSecondNum(firstNumList, secondNumList)
        resultNum = searchNum
        if case == 3:
            thirdNumList = self.getThirdNumListCase3(searchNum)
        else:
            thirdNumList = self.getThirdNumListCase12(searchNum)
        resultNum = numCalculator.getResultNumCase(thirdNumList)
        return resultNum
              
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
            self.gongoNumberDict1[gongoName] = self.calResultNumByCase(1)
            print("START FIRST CASE PROCESS...")
        else:
            print("NOT ENOUGH DATA...")
        self.closeAnalysisProgram()
            
    def searchSecondCaseNumber(self, gongoName):
        self.clickAnalysisProgramBtn()
        totalNum = self.getSecondCaseTotalNum()
        print("* SECOND CASE TOTAL NUM :", totalNum)
        if totalNum >= 30:
            self.gongoNumberDict2[gongoName] = self.calResultNumByCase(2)
            print("START SECOND CASE PROCESS...")
        else:
            print("NOT ENOUGH DATA...")
        self.closeAnalysisProgram()
            
    def searchThirdCaseNumber(self, gongoName):
        self.clickAnalysisProgramBtn()
        totalNum = self.getThirdCaseTotalNum()
        print("* THIRD CASE TOTAL NUM :", totalNum)
        if totalNum >= 30:
            self.gongoNumberDict3[gongoName] = self.calResultNumByCase(3)
            print("START THIRD CASE PROCESS...")
        else:
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
        pageUrl = "http://www.brbid.co.kr/Back_Office/C_Analysis/member004_01_sub.html?rdoFindDate=FinishDTime&txtSDate=" + self.startDt + "&txtEDate=" + self.endDt + "&lstMasterID=brbid&iKind=&rdoFindWord=BM.BidName&txtFindWord=&txtArea=&txtKind="
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
    pw = input(">> Enter Password :").strip()
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