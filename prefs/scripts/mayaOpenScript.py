import maya.cmds as cmds
import os
import shutil
from sys import path
from importlib import reload
import maya.mel as mel
import hashlib

mayaScript=cmds.internalVar(userScriptDir=True)
start="/userSetup.py"

target  = mayaScript +"/Abin_Tools"
    
source=getPlace

winds = 'install_UI'
def setVtxMainWins():
    if cmds.window(winds,ex = True):
        cmds.deleteUI(winds)
        
    cmds.window(winds , t = u'install_Tool')
    cmds.columnLayout( adjustableColumn=True,rowSpacing=10,w=200)
    cmds.progressBar("install_progressControl",maxValue=10, width=200)
    cmds.showWindow(winds)

setVtxMainWins()


skip_dirs =[r'prefs\Tools']
skip_files = ['.WeDrive']  
init_files=[r'prefs\setting\maya_abin_tools.ini']


def calculate_file_hash(file_path):
    """计算文件的哈希值"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        # 分块读取文件，避免内存不足
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def are_files_identical(file1, file2):
    """判断两个文件是否相同"""
    return calculate_file_hash(file1) == calculate_file_hash(file2)

def copy_file(src, dst):
    """复制文件，如果目标文件存在则替换"""
    shutil.copy2(src, dst)

def main(file1, file2):
    if os.path.exists(file2):
        if not are_files_identical(file1, file2):
            print(f"文件不同，正在复制 {file1} 到 {file2}...")
            copy_file(file1, file2)
    else:
        copy_file(file1, file2)

maxP=0
def sum_files(src, dst, skip_dirs=skip_dirs,skip_files=skip_files):
    global maxP  # 声明 maxP 为全局变量
    for skin in skip_dirs:
        if skin in src:
            return
    
    for item_name in os.listdir(src):
        src_item = os.path.join(src, item_name)
        dst_item = os.path.join(dst, item_name)
        
        if os.path.isdir(src_item):
            # 如果是目录，则递归调用
            sum_files(src_item, dst_item)
        elif os.path.isfile(src_item):
            # 如果是文件，检查目标目录中是否存在同名文件
            if item_name not in skip_files:
                maxP += 1

src_dir = os.path.abspath(source)
dst_dir = os.path.abspath(target)   

sum_files(src_dir,dst_dir)
print("总进度",maxP)
cmds.progressBar("install_progressControl", edit=True,endProgress=1)
cmds.progressBar("install_progressControl", edit=True,minValue=0,maxValue=maxP)

def copy_directory(src, dst,skip_dirs=skip_dirs,skip_files=skip_files):
    for skin in skip_dirs:
        if skin in src:
            # print(f"Skipped: {src}")
            return
    
    if not os.path.exists(dst):
        os.makedirs(dst)
    # print(f"copy: {src}")
    for item_name in os.listdir(src):
        src_item = os.path.join(src, item_name)
        dst_item = os.path.join(dst, item_name)
        
        if os.path.isdir(src_item):
            # 如果是目录，则递归调用
            copy_directory(src_item, dst_item)
        elif os.path.isfile(src_item):
            # 如果是文件，检查目标目录中是否存在同名文件
            if item_name not in skip_files:
                main(src_item, dst_item)
                cmds.progressBar("install_progressControl", edit=True, step=1)
            # if os.path.exists(dst_item):
            #     # 删除目标目录中的旧文件
            #     os.remove(dst_item)
            # # 复制新文件
            # shutil.copy2(src_item, dst_item)


#####


copy_directory(src_dir, dst_dir)

source_file = target+start
destination_file = mayaScript+start

isTest=False
if not os.path.isfile(destination_file) or isTest:
        # 如果不存在，则复制文件
        shutil.copy2(source_file, destination_file)  # copy2 会尝试保留文件的元数据（如时间戳）
        print(f"文件已复制: {source_file} -> {destination_file}")
else:
        with open(source_file, 'r', encoding='utf-8') as source_file:
            content = source_file.read()

        if not "Abin_Tools" in content:
            # 打开文件以追加模式写入
            with open(destination_file, 'a', encoding='utf-8') as file:
                # 添加新的文本内容到文件末尾
                file.write('\n# AbinTool启动项\n')
                file.write(content)
            # print(f"文件已存在: {destination_file}")

'''
adv5插件
'''
adv_plug=mayaScript+"Abin_Tools/scripts/AdvancedSkeleton5.mel"
if not os.path.exists(adv_plug):
    print("\n-------------------安装adv插件-----------------")
    adv_path=source+"/prefs/Tools/AdvancedSkeleton5/install.mel"
    mel.eval(' source \"{}\" '.format(adv_path))

'''
studiolibrary插件
'''
studiolibrary_plug=mayaScript+"Abin_Tools/scripts/studiolibrary.py"
if not os.path.exists(studiolibrary_plug):
    print("\n-------------------安装studiolibrary插件-----------------")
    studiolibrary_path=source+"/prefs/Tools/studiolibrary-2.9.6.b3/install.mel"
    mel.eval(' source \"{}\" '.format(studiolibrary_path))


PATH=target+"/prefs/scripts"
if PATH not in path:
    path.append(PATH)
import setIcon
import MYMAYA
reload(setIcon)
reload(MYMAYA)

MYMAYA.SAVE.QSETTING.setValue(MYMAYA.SAVE.SOURCE, source+"/install.mel")

if cmds.window(winds,ex = True):
        cmds.deleteUI(winds)