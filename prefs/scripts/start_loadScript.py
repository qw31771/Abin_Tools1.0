import maya.mel as mel
import maya.cmds as cmds
import MYMAYA
import os
from shutil import copy2
from sys import path

#当前maya版本的本地路径
_path=mel.eval("getenv \"MAYA_LOCATION\" ")


#找到。mll文件和。py文件
# def find_mll_files(directory):
#     mll_files = []
#     py_files = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.mll'):
#                 mll_files.append([os.path.join(root, file),file])
#                 # mll_files.append(file)
#             elif file.endswith('.py'):
#                 if root not in py_files:
#                     py_files.append(root)
#     return mll_files , py_files

# mll,py=find_mll_files(MYMAYA.PATH.TOOLS)

# dst_dir=_path+"/bin/plug-ins"
# localScript=os.listdir(dst_dir)
# for i in mll:
#     if i[1] not in localScript:
#         dst_file = os.path.join(dst_dir, os.path.basename(i[0]))
#         print("复制插件到本地插件文件夹",i[1])
#         copy2(i[0], dst_file)
#         if not cmds.pluginInfo(i, query=True, loaded=True):
#             cmds.loadPlugin(i)
#             print("加载插件",i[1])

# for i in py:
#     if i not in path:
#         path.append(i)
#         print("添加到环境变量",i)

# #加载特殊加载的文件夹
# files=[MYMAYA.PATH.TOOLS]
# for f in files:
#     for item in os.listdir(f):
#         item_path = os.path.join(f, item)
#         if os.path.isdir(item_path):
#             for tool in os.listdir(item_path):
#                 tool_path=os.path.join(item_path, tool)
#                 if os.path.isdir(tool_path):
#                     if tool_path not in path:
#                         path.append(tool_path)
#                         print("添加到环境变量",tool_path)

#全部文件夹
def find_all_directories(target_dir):
    directories = []
    for dirpath, dirnames, _ in os.walk(target_dir):
        # 移除 "__pycache__" 目录
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for dirname in dirnames:
            full_path = os.path.join(dirpath, dirname)
            directories.append(full_path)
    return directories

#一级文件夹
def get_first_level_directories(target_dir):
    directories = []
    with os.scandir(target_dir) as entries:
        for entry in entries:
            if entry.is_dir() and entry.name != "__pycache__":
                directories.append(entry.path)
    return directories

tools=find_all_directories(MYMAYA.PATH.TOOLS)
FILES=tools
for file in FILES:
    if os.path.exists(file):
        if file not in path:
            path.insert(0, file)  # 插入到最前优先加载
            print("已添加环境变量: {}".format(file))
    else:
        print("警告: 路径不存在 {}".format(file))
