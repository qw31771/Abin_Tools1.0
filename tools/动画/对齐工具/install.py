# -*- coding: utf-8 -*-
import sys
import winreg
string = r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, string)
location, _type = winreg.QueryValueEx(handle, 'Personal')
path = location + u"/maya/2019/zh_CN/scripts/对齐工具"
sys.path.append(path)
import maya.cmds as cmds
import  alignsUI as   aa
from imp  import  reload
reload(aa)
main = aa.anign_UI()
main.show()
