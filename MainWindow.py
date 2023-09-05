# @Author      : Duhongkai
# @Time        : 2023/5/13 18:35
# @Description : 程序主函数

import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import datetime
import os
import json
import shutil
from first_page.page1_widget import Ui_first_page
from fourth_page.page4_widget import Ui_fourth_page
from action import Main_Action,page1_action,page4_action

class Main(QMainWindow):
    def __init__(self,root_file):
        super().__init__()
        self.root_file = root_file
        self.init_ui()
        self.init_menu()
        self.init_tabWidget()
        self.center_window()

    def init_ui(self):
        # self.setGeometry(300, 300, 1100, 700)
        self.setFixedSize(1200,800)
        self.setWindowTitle('数据存储与处理软件')
        week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        self.statusBar().showMessage(f"今天是：{datetime.datetime.now().strftime('%Y年%m月%d日')} {week_list[datetime.datetime.now().weekday()]}")
        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        self.setStyleSheet(self.load_qss(root_file+'static/qss/basic.qss'))

    def init_menu(self):
        menubar = self.menuBar()
        settingMenu = menubar.addMenu('设置')
        aboutMenu = menubar.addMenu('关于')
        helpMenu = menubar.addMenu('帮助')
        moreMenu = menubar.addMenu('更多')

        imgAction = QAction(QIcon(f'{self.root_file}static/img/img_icon.png'),'图像默认设置', self)
        imgAction.setShortcut('Alt+I')
        imgAction.triggered.connect(lambda x: Main_Action.img_action(self.root_file))
        settingMenu.addAction(imgAction)

        tabAction = QAction(QIcon(f'{self.root_file}static/img/table_icon.png'),'表格默认设置', self)
        tabAction.setShortcut('Alt+T')
        # tabAction.triggered.connect(lambda x: Main_Action.table_action(self.root_file))
        settingMenu.addAction(tabAction)

        movieAction = QAction(QIcon(f'{self.root_file}static/img/movie_icon.png'),'视频默认设置', self)
        movieAction.setShortcut('Alt+V')
        # movieAction.triggered.connect(lambda x: Main_Action.video_action(self.root_file))
        settingMenu.addAction(movieAction)


    def init_tabWidget(self):
        self.tabWidget = QTabWidget(self)
        # tabWidget.resize(1200,1080)
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        self.tab4 = QWidget(self)
        self.tabWidget.addTab(self.tab1, '图像处理')
        self.tabWidget.addTab(self.tab4, '视频流处理')
        self.tabWidget.addTab(self.tab2, '数据表显示')
        self.tabWidget.addTab(self.tab3, '统计图显示')
        self.setCentralWidget(self.tabWidget)
        self.tabp1()
        self.tabp4()
    def tabp1(self):
        # 初始化第一个界面
        self.first_page = Ui_first_page(self.tab1,self.root_file)
        self.first_page.handle_img_signal.connect(page1_action.slide_action)
        self.first_page.left_bn_signal.connect(page1_action.left_bn_action)

    def tabp4(self):
        # 初始化第四个界面
        fourth_page = Ui_fourth_page(self,self.tab4,self.root_file)
        fourth_page.handle_img_signal.connect(page4_action.slide_action)
        fourth_page.left_bn_signal.connect(page4_action.left_bn_action)
        fourth_page.video_bn_signal.connect(page4_action.video_bn_action)

    def load_qss(self,qss_file):
        with open(qss_file,'r') as file:
            qss_data = file.read()
        return qss_data

    def center_window(self):
        primary_screen = QGuiApplication.primaryScreen()
        screen_geometry = primary_screen.availableGeometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

def create_main_file(root_dir):
    if not os.path.exists(root_dir+'resources/img'): #判断所在目录下是否有该文件名的文件夹
        os.makedirs(root_dir+'resources/img')
        shutil.copy('static/img/default_img.jpg', root_dir + 'resources/default_img.jpg')
        shutil.copy('static/video/default_video.mp4', root_dir + 'resources/default_video.mp4')
        shutil.copytree('static/img/',root_dir+'static/img/')
        os.makedirs(root_dir+'static/qss')
        shutil.copy('qss/basic.qss',root_dir+'static/qss/basic.qss')
    if not os.path.exists(root_dir + 'log'):  # 判断所在目录下是否有该文件名的文件夹
        os.mkdir(root_dir + 'log')
    if not os.path.exists(root_dir + 'config'):
        os.mkdir(root_dir + 'config')
        init_config(root_dir+'config/setting.jsonl')
    if not os.path.exists(root_dir + 'tmp'):
        os.mkdir(root_dir + 'tmp')
        shutil.copy('static/img/tmp.jpg',root_dir + 'tmp/tmp.jpg')


def init_config(file):
    """
        default_save_location:默认图片保存位置
    """
    content = {"img":{"default_save_location":"D:/203demo/resources/img"}}
    with open(file,'w') as f:
        f.write(json.dumps(content))

if __name__ == '__main__':
    root_file = "F:/203demo/"
    create_main_file(root_file)
    app = QApplication(sys.argv)
    ex = Main(root_file)
    ex.show()
    sys.exit(app.exec())

"""
plotdigitizer  figures/graph_with_grid.png -p 200,0 -p 1000,0 -p 0,50 -l 269,69 -l 1789,69 -l 82,542 --plot figures/graph_with_grid.result.png
"""