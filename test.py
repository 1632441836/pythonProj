# -*- coding:utf-8 -*-
import chardet
import subprocess
import re

strA = '你好'
strB = u'你好'
s = subprocess.check_output('echo ' + strB, shell=True)
print s

s = '''
Sending        CardPirate/trunk/cocos2d-x-2.2.3/projects/20160105_push_1.0.0/Resources/script/module/specialTreasure/SpecTreaRefineCtrl.lua
Sending        CardPirate/trunk/cocos2d-x-2.2.3/projects/20160105_push_1.0.0/Resources/script/module/specialTreasure/SpecTreaRefineView.lua
Transmitting file data ..
Committed revision 196476.
'''
match = re.search(r'(?<=Committed revision )\d{6}(?=\.)', s)
if match:
    print match.group()