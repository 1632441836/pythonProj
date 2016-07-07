# -*- coding:utf-8 -*-

import xml.etree.cElementTree as ET
import os

splitChars = [';', ',', '|']
connectChars = [';,',';;',';|',',;',',,',',|','|,','||','|;',]

xmlPath = r"/Users/lvnanchun/Documents/workspace/正式策划案/导出工具表/导出XML表"

xmlFiles = {}
# xmlFiles = glob.glob(r'/Users/lvnanchun/Documents/workspace/正式策划案/导出工具表/导出XML表/*.xml')
for file in os.listdir(xmlPath):
    if file.find(".xml") != -1:
        xmlFiles[xmlPath + '/' + file] = file.split('.')[0]

for xmlFile, fileName in xmlFiles.items():
    print xmlFile
    dbTree = ET.ElementTree(file=xmlFile)

    root = dbTree.getroot()

    for rootChild in root:
        for key, value in rootChild.attrib.items():
            if isinstance(value, str) and value != '':
                for splitChar in splitChars:
                    if '' in value.split(splitChar):
                        print fileName + ':' + key + ':' + value
                        break
                    for string in connectChars:
                        if (value.find(string) != -1):
                            print fileName + ':' + key + ':' + value