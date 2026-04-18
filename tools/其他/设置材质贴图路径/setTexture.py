from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CustomDialog(QtWidgets.QDialog):
    dlg_instance = None
def __init__(self, parent=maya_main_window()):
    super(CustomDialog, self).__init__(parent)

    self.setWindowTitle("Abin_绑定工具")
    self.setMinimumSize(600, 400)
    self.setWindowFlags(QtCore.Qt.Window)

    self.create_widgets()
    self.create_layout()
    self.create_connections()

def create_widgets(self):
    pass

def create_layout(self):
    pass

def create_connections(self):
    pass

dlg_instance=None
@classmethod
def showWindow(cls):
    if not cls.dlg_instance:
        cls.dlg_instance = CustomDialog()

    if cls.dlg_instance.isHidden():
        cls.dlg_instance.show() 
    else:
        cls.dlg_instance.raise_()
        cls.dlg_instance.activateWindow()

# if __name__ == "__main__":
#     try:
#         dialog.close()
#         dialog.deleteLater()
#     except:
#      pass

#     dialog = CustomDialog()
#     dialog.show()














# def checkRigJointUI():
#     winds = 'setTexture_UI'
#     if cmds.window(winds,ex = True):
#         cmds.deleteUI(winds)
        
#     cmds.window(winds , t = u'修改材质贴图路径1.0')
#     cmds.formLayout( "texturePathForm",nd=100)
#     separator01=cmds.separator( style='out' )
#     text=cmds.text("text",l="路径",h=30)
#     textF=cmds.textField("texturePath",w=400,h=30)
#     setPath=cmds.button("setPath",w=80,l="选择文件夹",h=30)


#     setBtn=cmds.button("set",l="设置！")

    
#     cmds.formLayout("texturePathForm",e=1,
#     af=[
#         (separator01, "left", 5), (separator01, "top", 10),(separator01, "right", 5),
#         (text, "left", 5),(setPath, "right", 5),
#         (setBtn, "left", 5),(setBtn, "right", 5),
        
#     ],
#     attachControl=[
#         (text, "top", 10,separator01),
#         (textF, "top", 10,separator01),(textF, "left", 5,text),(setPath, "top", 10,separator01),(textF, "right", 5,setPath),
#         (setBtn, "top", 5,textF),
#     ],
#     )

#     cmds.showWindow(winds)






# sl=cmds.ls(type="file")
# temp_path="F:\提交文件1026\角色\CHA_AGT_CL_AT\FPP\Model"
# path=temp_path.replace('\\','/')
# for i in sl:
#     file=cmds.getAttr(i+".fileTextureName")
#     name=file[file.rfind("/")+1:len(file)]
#     setPath=path+"/"+name
#     print(temp_path)
#     cmds.setAttr(i+".fileTextureName",setPath,type="string")
    

# import setTexture
# from importlib import reload
# load_ui=reload(setTexture)
# load_ui.checkRigJointUI()