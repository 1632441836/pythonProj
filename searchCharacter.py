# -*- coding:utf-8 -*-

import xml.etree.cElementTree as ET
import glob
import os

splitChars = [';', ',', '|']
# xmlPath = r"/Users/lvnanchun/Documents/workspace/CardPirate/tools/XmlToScript.unixlike/xml_db"
xmlPath = r"/Users/lvnanchun/Documents/workspace/正式策划案/导出工具表/导出XML表"

xmlFiles = {}
# xmlFiles = glob.glob(r'/Users/lvnanchun/Documents/workspace/正式策划案/导出工具表/导出XML表/*.xml')
for file in os.listdir(xmlPath):
    if file.find(".xml") != -1:
        xmlFiles[xmlPath + '/' + file] = file.split('.')[0]

splitStrList = {}

# 排序输出字符串
def sortString(srcStr):
    tarStr = ""
    for character in splitChars:
        if character in srcStr:
            tarStr += character
    return tarStr

# 遍历xml表将里面出现;|,的字段的文件名和字段名放进splitStrList这个字典里面
for xmlFile, fileName in xmlFiles.items():
    dbTree = ET.ElementTree(file=xmlFile)
    splitStrList[fileName] = {}

    root = dbTree.getroot()

    for rootChild in root:
        for key, value in rootChild.attrib.items():
            if isinstance(value, str):
                for splitChar in splitChars:
                    if value.find(splitChar) != -1:
                        if key in splitStrList[fileName]:
                            if splitStrList[fileName][key].find(splitChar) == -1:
                                splitStrList[fileName][key] += splitChar
                        else:
                            splitStrList[fileName][key] = splitChar

for key, value in splitStrList.items():
    for name, char in value.items():
        sortedChar = sortString(char)
        print key + ":" + name + ":" + sortedChar
        linesList = []
        cfgFile = open(xmlPath + '/' + key + '.cfg', "r+")
        for line in cfgFile.readlines():
            if line.find("string") != -1:
                line = line[0:line.find("string")+6]
                if line.find(name + '=') == 0:
                    line += sortedChar
                line += '\r\n'
                print line
            linesList.append(line)
        cfgFile.close()
        cfgFile = open(xmlPath + '/' + key + '.cfg', "w+")
        cfgFile.writelines(linesList)
        cfgFile.close()




