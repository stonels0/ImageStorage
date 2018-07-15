# -*- coding: utf-8 -*-
"""
Created on Tue Dec 08 16:34:59 2015

@author: Administrator
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os
import math
from shutil import move
from easydict import EasyDict as edict
import json
import pdb

QTextCodec.setCodecForTr(QTextCodec.codecForName('utf8'))

glb_screen_NO = 0                   # screen_id
glb_file_name = ''
glb_file_path = ''
glb_class_path = ''
glb_imgNum_OneScn = 20      # image number of per screen
glb_screen_num = 0                 # the number of screen
all_ImgNames = []                    # all image name list
glb_synset_id = {}

glb_class_dict = {}
glb_folders_list = []

glb_class_txt = './class_voc.json'
glb_folders_txt = './imagenet_folders.txt'

# the main window;
class ShowImgsWindow(QMainWindow):
    def __init__(self,parent = None):
        super(ShowImgsWindow,self).__init__(parent)
        self.setWindowTitle("Images Show")
        self.resize(800,800)        
        self.createActions()
        self.createMenus()
        self.createToolBars()

        # initial the folderlist;
        global glb_folders_txt
        global glb_folders_list
        global glb_class_txt
        global glb_class_dict
        with open(glb_folders_txt,'r') as fid:
            folders = fid.readlines()
        if os.path.exists(glb_class_txt):
            with open(glb_class_txt,'r') as f:
                glb_class_dict = json.load(f)
        else:
            glb_class_dict = {}
        
        glb_folders_list = folders[0].strip().split(',')
        glb_folders_list = glb_folders_list[0:-1]
        
        main_Widget = QWidget()        # the main widget;
        main_layout = QGridLayout(main_Widget) # the main layout
        ''' -- 添加基本信息布局 -- '''
        self.basci_widget = self.basicInfoLayout()
        main_layout.addWidget(self.basci_widget,0,0)        
        
        main_Widget.setLayout(main_layout)        
        self.setCentralWidget(main_Widget) # set up the central widget;

        
    def createActions(self):
        # open action
        self.fileOpenAct = QAction(QIcon("./icons/dir.png"),self.tr("打开"),self)
        self.fileOpenAct.setShortcut("Ctrl+F")
        self.fileOpenAct.setStatusTip(self.tr("选择一个文件夹"))
        self.connect(self.fileOpenAct,SIGNAL("triggered()"),self.slotOpenFile) # If the action been triggered, execute the slotOpenFile()
        
        # exit action
        self.exitAct = QAction(QIcon("./icons/2.png"),self.tr("退出"),self)
        self.exitAct.setShortcut("Ctrl+Q")
        self.exitAct.setStatusTip(self.tr("退出"))
        self.connect(self.exitAct,SIGNAL("triggered()"),self.close)     # If the action been triggered, execute the self.close()
        
        # next screen action
        self.nextScnAct = QAction(QIcon("./icons/next.png"),self.tr("下一屏"),self)
        self.nextScnAct.setShortcut("Page Down")
        self.connect(self.nextScnAct,SIGNAL("triggered()"),self.slotNextScn)    # If the action been triggered, execute the self.slotNextScn()
        self.prevScnAct = QAction(QIcon("./icons/prev.png"),self.tr("上一屏"),self)
        self.prevScnAct.setShortcut("Page Up")
        self.connect(self.prevScnAct,SIGNAL("triggered()"),self.slotPrevScn)    # If the action been triggered, execute the self.slotPrevScn()

        # save action
        self.fileSaveAct = QAction(QIcon("./icons/dir.png"),self.tr("保存"),self)
        self.fileSaveAct.setShortcut("Ctrl+S")
        self.fileSaveAct.setStatusTip(self.tr("save the result!!!"))
        self.connect(self.fileSaveAct,SIGNAL("triggered()"),self.slotSaveFile) # If the action been triggered, execute the slotOpenFile()        

    def createMenus(self):
        # file menu
        fileMenu = self.menuBar().addMenu(self.tr("文件"))
        fileMenu.addAction(self.fileOpenAct)
        fileMenu.addAction(self.exitAct)
        fileMenu.addAction(self.fileSaveAct)

        # edit menu
        EditMenu = self.menuBar().addMenu(self.tr("编辑"))
        EditMenu.addAction(self.prevScnAct)
        EditMenu.addAction(self.nextScnAct)
    
    def createToolBars(self):
        fileToolBar = self.addToolBar(self.tr("打开"))
        fileToolBar.addAction(self.fileOpenAct)
        editToolBar = self.addToolBar(self.tr("编辑"))
        editToolBar.addAction(self.prevScnAct)
        editToolBar.addAction(self.nextScnAct)
           
    def slotOpenFile(self):
        global glb_file_path
        s_dir = QFileDialog.getExistingDirectory(self,"Open file dialog", #"./")
                r"F:/expData/ImageNet_224_224") # s_dir : the selected path;
        all_fileName = os.listdir(str(s_dir))       # get all the file name;
        
        self.List_fileName.clear()                    # clear up the exist already;
        self.List_fileName.addItems(all_fileName) # add the items into the filename list;
#        setWidth = self.List_fileName.sizeHintForColumn(0)
        self.List_fileName.setMaximumWidth(120)

        glb_file_path = str(s_dir)

    def slotSaveFile(self):
        global glb_folders_list
        global glb_class_dict

        with open(glb_folders_txt,'w+') as f:
            for idx, folder in enumerate(glb_folders_list):
                f.write(folder+',')
        with open(glb_class_txt,'w+') as f:
            json.dump(glb_class_dict,f)
        last_folder_num = len(glb_folders_list)
        deal_folder_num = sum([len(item) for item in glb_class_dict.values()])
        QMessageBox.information(self,"Warning",self.tr("处理文件:{}\n剩余文件:{}\n共计:{}".format(deal_folder_num, last_folder_num, deal_folder_num+last_folder_num)))
        
    def slotPrevScn(self):
        global glb_screen_NO
        global glb_file_name  # the current folders;

        if glb_screen_NO == 0:
            QMessageBox.information(self,"Warning",self.tr("没有数据 ！"))
        else:
            glb_screen_NO = glb_screen_NO - 1
            if glb_screen_NO <= 0:
                glb_screen_NO = glb_screen_NO + 1
                QMessageBox.information(self,"Warning",self.tr("已经是第一屏"))
            else:
                img_path = os.path.join(glb_file_path, glb_file_name)
                img_info = [img_path,glb_screen_NO]                
                #img_info = [glb_file_path, glb_screen_NO]
                self.showImgsFunc(img_info)
                #self.Edit_ImgName.setText("")
            
    def slotNextScn(self):
        global glb_screen_NO
        global glb_file_name # the current folders;
        if glb_screen_NO == 0:
            QMessageBox.information(self,"Warning",self.tr("没有数据 ！"))
        else:
            glb_screen_NO = glb_screen_NO + 1
            if glb_screen_NO > glb_screen_num:
                glb_screen_NO = glb_screen_NO - 1
                QMessageBox.information(self,"Warning",self.tr("已经是最后一屏"))
            else:
                img_path = os.path.join(glb_file_path, glb_file_name)
                img_info = [img_path,glb_screen_NO]
                self.showImgsFunc(img_info)
                #self.Edit_ImgName.setText("")
    
    def basicInfoLayout(self):      # the basic info of all widgets
        ''' -- List -- '''
        #self.List_fileName = QListWidget()      # the widgets list;
        ''' -- up Layout -- ''' 
        basci_widget = QWidget()
        self.basic_Vlayout = QVBoxLayout()
        self.basic_Hlayout = QHBoxLayout()
        self.basci_upGrid1 = QGridLayout()    # the layout class;
        self.basci_upGrid2 = QGridLayout()
        #self.basci_upGrid.addWidget(self.List_fileName,0,0,10,1)    # the folder list;将List_fileName(QWidget)部件的行跨度设为9，列跨度设为10
        #self.basci_upGrid.addWidget(self.EditInfoLayout(),0,1,1,4) #,1,10 # the widget for modify;
        ''' -- main Layout -- ''' 
        bmain_layout = QGridLayout(basci_widget)
        bmain_layout.addLayout(self.basic_Vlayout,0,0)

        self.basic_Hlayout.addLayout(self.basci_upGrid1)
        self.basic_Hlayout.addLayout(self.basci_upGrid2)

        self.label_show = QLabel()
        self.label_show.setFixedWidth(800)
        self.label_show.setFixedHeight(20)
        self.label_show.setFont(QFont("Roman times",15,QFont.Bold))
        self.basic_Vlayout.addWidget(self.label_show)
        self.basic_Vlayout.addLayout(self.basic_Hlayout)


        basci_widget.setLayout(bmain_layout)
        # QListWidget的点击事件
        #self.List_fileName.itemClicked.connect(self.list_itemClick)         # corresponding to the left widget filelist; If the current folder is clicked, the right viewer will be show the images in the folder;
        self.show_imgs()
        self.show_classes()
        return basci_widget
    
    def show_imgs(self):
        global glb_screen_NO
        global glb_file_name
        global glb_screen_num
        global all_ImgNames
        global glb_file_path

        global glb_synset_id

        all_ImgNames = []

        if len(glb_folders_list) == 0:
            QMessageBox.information(self,"Warning",self.tr("已经是最后一文件夹"))
            self.slotSaveFile()
            return
        cur_folder = glb_folders_list[-1]
        #cur_folder = glb_folders_list.pop()   # imshow the last index of the listfolder;不应该在这pop，这次没点，岂不是没了;
        glb_file_name = cur_folder
        img_path = os.path.join(glb_file_path, cur_folder)
        all_imgName = os.listdir(img_path)               # get the sub-folder all images;
        img_num = len(all_imgName)                       #  the number of the folder images
        t_mod = (img_num - 1) % (glb_imgNum_OneScn - 1)
        glb_screen_num = int((img_num - 1)/(glb_imgNum_OneScn - 1))
        if t_mod != 0 or img_num < glb_imgNum_OneScn:
            glb_screen_num = glb_screen_num + 1     # if has the remainder, the screen number should add one screen
        glb_screen_NO = 1   # the current number of screen;     

        img_info = [img_path, glb_screen_NO]
        self.showImgsFunc(img_info) # image_info: the rootpath, the cur folder , and the screen_no        
        semantic_label = glb_synset_id.get(cur_folder)
        self.label_show.setText(self.tr(semantic_label))

    def show_classes(self):

        global glb_screen_num
        global all_ImgNames
        global glb_class_path

        
        img_path = glb_class_path 
        all_imgName = os.listdir(img_path)               # get the sub-folder all images;
        img_num = len(all_imgName)                       #  the number of the folder images
        
        glb_screen_NO = 1   # the current number of screen;     

        class_info = [glb_class_path, glb_screen_NO]
        self.showClassFunc(class_info) # image_info: the rootpath, the cur folder , and the screen_no                
    # QListWidget的点击事件， item can be get directly;
    def list_itemClick(self,item):  # select the itemClicked;
        global glb_screen_NO
        global glb_file_name
        global glb_screen_num
        global all_ImgNames
        all_ImgNames = []
        cur_item = str(item.text())        
        img_path = glb_file_path + '/' + cur_item       # cur_item means that the sub folder of the root dir;
        all_imgName = os.listdir(img_path)               # get the sub-folder all images;
        img_num = len(all_imgName)                       #  the number of the folder images
        t_mod = (img_num - 1) % (glb_imgNum_OneScn - 1)
        glb_screen_num = int((img_num - 1)/(glb_imgNum_OneScn - 1))
        if t_mod != 0 or img_num < glb_imgNum_OneScn:
            glb_screen_num = glb_screen_num + 1     # if has the remainder, the screen number should add one screen
        glb_screen_NO = 1   # the current number of screen;     
        glb_file_name = cur_item

        img_info = [glb_file_path, glb_file_name, glb_screen_NO]
        self.showImgsFunc(img_info) # image_info: the rootpath, the cur folder , and the screen_no
        self.Edit_ImgName.setText("")
        
    
    def showImgsFunc(self,img_info):
        self.ImgGrid_click = showImgsGrid(img_info)     # image show grid-window
        ''' -- 设置背景颜色 -- '''
        self.ImgGrid_click.setAutoFillBackground(True) # setup the auto fillbackground;
        palette_t = QPalette()
        palette_t.setColor(self.backgroundRole(),QColor(204,232,207)) # set the default background;
        self.ImgGrid_click.setPalette(palette_t)
        
        self.basci_upGrid1.addWidget(self.ImgGrid_click,1,1,9,10)        # 将ImgGrid_click部件的行跨度设为9，列跨度设为10
        #self.ImgGrid_click.toolBtn_clcEvent.connect(self.updateEditInfo) # #将传递的信号连接上处理函数


    def showClassFunc(self,class_info):
        palette_t = QPalette()
        palette_t.setColor(self.backgroundRole(),QColor(204,232,207)) # set the default background;

        # the classes of pascal voc;
        self.ClassGrid_click_c = showImgsGrid_CLASSES(class_info)
        self.ClassGrid_click_c.setAutoFillBackground(True)
        self.ClassGrid_click_c.setPalette(palette_t)
        self.basci_upGrid2.addWidget(self.ClassGrid_click_c,1,1,9,10)
        self.ClassGrid_click_c.toolBtn_clcEvent_affirm.connect(self.updateImg_classInfo)

    
    def EditInfoLayout(self):
        ''' -- Label -- ''' 
        label_Char = QLabel(self.tr("字符:"))
        self.label_Hint = QLabel()
        ''' -- Line Edit -- '''
        self.Edit_ImgName = QLineEdit()
        self.Edit_Unicode = QLabel()
        self.Edit_Char = QLineEdit()#QTextEdit()#
#        self.Edit_Char.setFixedHeight(30)
        self.Edit_Char.setFixedWidth(150)
        ''' -- Button -- '''
        btn_Edit = QPushButton(self.tr("修 改"))
        btn_Edit.setFixedWidth(80)
        btn_Delete = QPushButton(self.tr("删 除"))
        btn_Delete.setFixedWidth(80)
        
        edit_widget = QWidget()
        edit_HBox = QHBoxLayout(edit_widget)
#        edit_HBox.addWidget(self.Edit_ImgName)
        edit_HBox.addWidget(label_Char)
        edit_HBox.addWidget(self.Edit_Char)
        edit_HBox.addWidget(self.Edit_Unicode)
        edit_HBox.addWidget(btn_Edit)
        edit_HBox.addWidget(btn_Delete)
        edit_HBox.addWidget(self.label_Hint)
        edit_widget.setLayout(edit_HBox)
        btn_Edit.clicked.connect(self.Edit_Click)   # slot function
        btn_Delete.clicked.connect(self.Del_Click) # slot function
        return edit_widget

    def updateImg_classInfo(self,para_list):
        # #para_list 就是传递过来的参数；
        global glb_class_dict
        global glb_folders_list
        global glb_file_name

        objName = para_list[0]
        text_unic = para_list[1]

        cur_folder = glb_folders_list.pop()
        if cur_folder != glb_file_name:
            pdb.set_trace()
            print ('has error!!!')
        glb_class_dict.setdefault(objName,[]).append(glb_file_name)
        
        #cur_folder = glb_folders_list.pop()
        #temp_folder = glb_folders_list.pop()
        #index = glb_folders_list.index(cur_folder)
        #glb_folders_list.insert(index,temp_folder)
        self.show_imgs()
        self.raise_()  

    def updateEditInfo(self,para_list):
        # #para_list 就是传递过来的参数；
        objName = para_list[0]
        text_unic = para_list[1]
        self.Edit_ImgName.setText(str(objName))
        self.Edit_Unicode.setText(str(text_unic))
        self.Edit_Char.setText(unichr(int(str(text_unic))))
        self.label_Hint.setText("")
        self.raise_()  

    def  keyPressEvent(self,event):
        if event.key() == Qt.Key_Delete:
            self.Del_Click()
        elif event.key() == Qt.Key_Return:
            self.Edit_Click()
#        elif event.key() == Qt.Key_Enter:
#            self.Edit_Click()
    
    def Del_Click(self):    # slot function
        if str(self.Edit_ImgName.text()) == '':
            QMessageBox.information(self,"Information",self.tr("请选择图片"))
        else:
            dest_file = glb_file_path + '/../moved_images/'
            if not os.path.exists(dest_file):
                os.makedirs(dest_file)
            img_name = str(self.Edit_ImgName.text())    # self.Edit_ImgName = QLineEdit() , the image name;
            orig_file = glb_file_path + '/' + glb_file_name + '/' + img_name
            move(orig_file,dest_file) 
            self.label_Hint.setText(self.tr("删除成功！"))
            self.Edit_ImgName.setText("")
            self.updateImgNames(img_name)   # remove the image_name from the all_ImgNames list;
            img_info = [glb_file_path, glb_file_name, glb_screen_NO]
            self.showImgsFunc(img_info)          # show the images in the folder currently once again;
    
    def Edit_Click(self): # slot function
        if str(self.Edit_ImgName.text()) == '':
            QMessageBox.information(self,"Information",self.tr("请选择图片"))
        else:
#            QMessageBox.information(self,"Information","0")
            text_ch = self.tr(self.Edit_Char.text())#self.tr("我")#
            ''' -------------- '''
            ''' 这句主要是针对转成exe后的程序使用，.text()返回的其实是QString类型的 
                在这个环境下，这句话运行不成功。环境自动将Qstring转成Unicode了'''
#            text_ch = unicode(self.Edit_Char.text().toUtf8(),encoding = "utf-8")
            ''' -------------- '''
#            QMessageBox.information(self,"Information",str(type(self.Edit_Char.text())))
#            QMessageBox.information(self,"Information",self.tr(text_ch))
            try:
                text_unic = ord(unicode(text_ch))#ord(u'\u6211')#
            except TypeError:
                QMessageBox.information(self,"Information","TypeError")
            self.Edit_Unicode.setText(str(text_unic))
            dest_file = glb_file_path + '/' + str(text_unic)
            if not os.path.exists(dest_file):
                os.makedirs(dest_file)
            img_name = str(self.Edit_ImgName.text())
            orig_file = glb_file_path + '/' + glb_file_name + '/' + img_name    # the image path;
            move(orig_file,dest_file) 
            self.label_Hint.setText(self.tr("修改成功！"))
            self.Edit_ImgName.setText("")
            self.updateImgNames(img_name)   # update the all_ImgNames;
            img_info = [glb_file_path,glb_file_name,glb_screen_NO]
            self.showImgsFunc(img_info)         # show the images in the folder once again;
            
    # update the all_ImgNames;
    def updateImgNames(self,img_name):
        global all_ImgNames
#        all_ImgNames.remove(img_name)
        temp_name = all_ImgNames.pop()
        img_index = all_ImgNames.index(img_name) # lookup the target object index, if not exist, then raise the error;
        all_ImgNames[img_index] = temp_name        # firstly, the list pop the object; secondly, repeat the object to the desindex; 
    ''' -------------- '''
    ''' 这个函数主要是针对转成exe后的程序使用，用于清空内存 '''
#    def cleanUp(self):
#        for i in self.__dict__:
#            item = self.__dict__[i]
#            clean(item)
    ''' -------------- '''

''' ----- Image Grid Part ------ '''
class showImgsGrid(QWidget):
    ''' -- 参数是路径以及当前文件夹的名字 -- '''
    # #list表示传递的参数是list格式
    toolBtn_clcEvent = pyqtSignal(list)
    def __init__(self,img_info,parent = None):
        global all_ImgNames
        super(showImgsGrid,self).__init__(parent)
        file_path = img_info[0]
        #file_name = img_info[1]
        screen_NO = img_info[1]
        #img_path = file_path + '/' + file_name
        img_path = file_path

        if img_path == '/':
            return
        elif img_path != '/' and all_ImgNames == []:
            all_ImgNames = os.listdir(img_path) # get the all images in the folders;
        
        splitted_ImgNames = self.split_ImgNames(all_ImgNames)   # according to the screen and img_num_screen_one, return the display listname;

        img_pos = []

        col_num = 4
        row_num = 5
        for row in range(0,row_num):
            for col in range(0,col_num):
                img_pos.append((row,col))
                
        grid_layout = QGridLayout(self)         # use the grid-layout to show the images;    
        j = 0
        for name in splitted_ImgNames[screen_NO - 1]:
            toolBtn_img = QToolButton()
            toolBtn_img.setText(str(name))#(str(j))#
            toolBtn_img.setObjectName(str(name))
            temp_imgPath = img_path + '/' + name
            toolBtn_img.setIcon(QIcon(temp_imgPath))
            toolBtn_img.setIconSize(QSize(140,100))
            toolBtn_img.setAutoRaise(False)
            toolBtn_img.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            grid_layout.addWidget(toolBtn_img,img_pos[j][0],img_pos[j][1])
            j = j + 1
            #toolBtn_img.clicked.connect(lambda:self.showEditDialog(file_name))
            toolBtn_img.setFocusPolicy(Qt.TabFocus)
            
        self.setLayout(grid_layout)
    
    def showEditDialog(self,file_name):
        sending_btn = self.sender()
        if int(str(sending_btn.text())) <= -1:
            sending_btn.setText(str(int(str(sending_btn.text()))-1))
#            QMessageBox.information(self,"Information",self.tr("已经处理过"))
        else:
            objName = str(sending_btn.objectName())
            text_unic = str(file_name)
            sending_btn.setText("-1")
            self.toolBtn_clcEvent.emit([objName,text_unic]) # emit the sigal to the out class;#传递参数
        
    def split_ImgNames(self,all_ImgNames):
#        img_Names = os.listdir(img_path)
        img_Names = all_ImgNames
        GtImg = img_Names[0]
        img_Names = img_Names[1:]
        img_num = len(img_Names)
        imgNum_OneScn = glb_imgNum_OneScn - 1
        stop_points = range(0,img_num,imgNum_OneScn)  # [start,end] and the scan,that's mean the step;
        if stop_points[-1] != img_num - 1:          # img_num: the index of the last item;
            stop_points.append(img_num - 1)     # non-entire screen, the last screen endindex is the all_ImgName last index;
        splitted_ImgNames = []                          # splitted_ImgNames is the array of array, the sub-array is the split filelist;
        if img_num == 0:
            splitted_ImgNames.append([GtImg])
            return splitted_ImgNames
        if img_num == 1:
            splitted_ImgNames.append([GtImg,img_Names[0]])
            return splitted_ImgNames
        for i_s in range(len(stop_points)-1):
            temp_subName = [GtImg] + img_Names[stop_points[i_s]:(stop_points[i_s+1])]
            splitted_ImgNames.append(temp_subName)
        if len(splitted_ImgNames[-1]) < glb_imgNum_OneScn:
            splitted_ImgNames[-1].append(img_Names[-1])
        else:
            splitted_ImgNames.append([img_Names[-1]])
        return splitted_ImgNames

class showImgsGrid_CLASSES(QWidget):
    """docstring for showImgsGrid_CLASSES"""
    ''' -- 参数是路径以及当前文件夹的名字 -- '''
    # #list表示传递的参数是list格式
    toolBtn_clcEvent_affirm= pyqtSignal(list)
    def __init__(self, class_info, parent = None):
        super(showImgsGrid_CLASSES, self).__init__()
        class_path = class_info[0]     # the parent folder of image class;
        class_names = os.listdir(class_path)

        self.img_class = [os.path.join(class_path, img_name) for img_name in class_names]

        row_num = 3
        img_pos = []
        col_num = int(math.ceil(len(self.img_class) / row_num))
        for row in range(0, row_num):
            for col in range(0, col_num):
                img_pos.append((row, col))

        grid_layout = QGridLayout(self)
        j = 0

        for name in class_names:
            toolBtn_img = QToolButton()
            toolBtn_img.setObjectName(name.strip().split('.')[0])
            temp_imgPath = os.path.join(class_path,name)
            toolBtn_img.setIcon(QIcon(temp_imgPath))
            toolBtn_img.setIconSize(QSize(120, 150))
            toolBtn_img.setAutoRaise(False)
            toolBtn_img.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            grid_layout.addWidget(toolBtn_img, img_pos[j][0], img_pos[j][1])
            j = j+1
            toolBtn_img.clicked.connect(lambda: self.showAffirmDialog())            #$$%$%$%^#$^&%^%$&^($)
            toolBtn_img.setFocusPolicy(Qt.TabFocus)

    def showAffirmDialog(self):
        global glb_class_dict
        sending_btn = self.sender()

        objName = str(sending_btn.objectName())
        text_unic = objName
        #sending_btn.setText("-1")
        sending_btn.setText(str(len(glb_class_dict.setdefault(objName,[]))+1))
        self.toolBtn_clcEvent_affirm.emit([objName,text_unic]) # emit the sigal to the out class;#传递参数

        

''' -------------- '''
''' 这个函数主要是针对转成exe后的程序使用，用于清空内存 '''
#def cleanUp(item):
#    if isinstance(item,list) or isinstance(item, dict):
#        for _ in range(len(item)):
#            clean(item.pop())
#    else:
#        try:
#            item.close()
#        except (RuntimeError, AttributeError):
#            pass
#        try:
#            item.deleteLater()
#        except (RuntimeError, AttributeError):
#            pass
''' -------------- '''

def get_folders():
    global glb_file_path
    folderlist = getfolderlist_current(glb_file_path)
    filename = './imagenet_folders.txt'
    with open(filename,'a+') as f:
        for idx, folder in enumerate(folderlist):
            f.write(folder+',')


def getfolderlist_current(filepath):
    return [_ for _ in os.listdir(filepath) if os.path.isdir(os.path.join(filepath,_))]
def getfolderlist_1000():
    with open('./synset/synsets.txt') as f:
        filelist = f.readlines()
    with open('./label_imagenet/image_test.txt','w+') as f:
        for i,folder in enumerate(filelist):
            f.write(folder.strip()+',')
        print('the number of image folder is:{}'.format(i+1))

def loadmap(filepath):
    synsetmap = {}
    assert os.path.exists(filepath)
    with open(filepath, 'r') as f:
        while True:
            lines = f.readline()
            if not lines:
                break
                pass
            p_key = lines.strip().split(' ')[0]
            p_value = lines[len(p_key):].strip()
            synsetmap[p_key]=p_value
    return synsetmap

if __name__ == "__main__":
    import sys
    #glb_file_path = 'E:/Lishi/Datasets/99-Source/ImageNet/fall11_whole'
    #get_folders()
    #getfolderlist_1000()
    #pdb.set_trace()
    filepath = './synset/synset_words.txt'
    glb_synset_id = loadmap(filepath)
    glb_class_txt = './label_imagenet/image_test.json'
    glb_folders_txt = './label_imagenet/image_test.txt'
    glb_file_path = r"E:/Lishi/Datasets/99-Source/ImageNet/fall11_whole" 
    glb_class_path = "./20-classes" 

    app = QApplication(sys.argv)    
    app.aboutToQuit.connect(app.deleteLater) 
    
    main = ShowImgsWindow()
    main.show()

    ''' -------------- '''
    ''' 这句主要是针对转成exe后的程序使用，用于清空内存 
        在spyder下运行，是上面那句，调用app.deletelater'''
    #app.aboutToQuit.connect(main.cleanUp)
    ''' -------------- '''
   
    sys.exit(app.exec_())
   