# Form implementation generated from reading ui file 'first_page_search.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QStringListModel, QDir
from PyQt6.QtGui import QFileSystemModel, QPixmap
from PyQt6.QtWidgets import QDialog
import os


class Search_file_dialog(QDialog):
    def __init__(self,root_path,cur_page,parent_page):
        super().__init__()
        self.cur_page = cur_page
        self.parent_page = parent_page
        self.root_path = root_path
        self.setupUi()
        self.setStyleSheet(self.load_qss(self.root_path + 'static/qss/basic.qss'))

    def setupUi(self):
        self.setObjectName("Dialog")
        self.setFixedSize(650, 456)
        self.widget = QtWidgets.QWidget(parent=self)
        self.widget.setGeometry(QtCore.QRect(2, 2, 651, 451))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.start_label = QtWidgets.QLabel(parent=self.widget)
        self.start_label.setObjectName("start_label")
        self.horizontalLayout.addWidget(self.start_label)
        self.start_time = QtWidgets.QDateTimeEdit(parent=self.widget)
        self.start_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 1, 1), QtCore.QTime(0, 0, 0)))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_time.sizePolicy().hasHeightForWidth())
        self.start_time.setSizePolicy(sizePolicy)
        self.start_time.setObjectName("start_time")
        self.start_time.setCalendarPopup(True)
        self.horizontalLayout.addWidget(self.start_time)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.ip = QtWidgets.QLabel(parent=self.widget)
        self.ip.setObjectName("ip")
        self.horizontalLayout_4.addWidget(self.ip)
        self.ip_edit = QtWidgets.QLineEdit(parent=self.widget)
        self.ip_edit.setObjectName("ip_edit")
        self.horizontalLayout_4.addWidget(self.ip_edit)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.user = QtWidgets.QLabel(parent=self.widget)
        self.user.setObjectName("user")
        self.horizontalLayout_3.addWidget(self.user)
        self.user_edit = QtWidgets.QLineEdit(parent=self.widget)
        self.user_edit.setObjectName("user_edit")
        self.horizontalLayout_3.addWidget(self.user_edit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.end_label = QtWidgets.QLabel(parent=self.widget)
        self.end_label.setObjectName("end_label")
        self.horizontalLayout_2.addWidget(self.end_label)
        self.end_time = QtWidgets.QDateTimeEdit(parent=self.widget)
        self.end_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2030, 1, 1), QtCore.QTime(0, 0, 0)))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.end_time.sizePolicy().hasHeightForWidth())
        self.end_time.setSizePolicy(sizePolicy)
        self.end_time.setObjectName("end_time")
        self.end_time.setCalendarPopup(True)
        self.horizontalLayout_2.addWidget(self.end_time)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.submit = QtWidgets.QPushButton(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit.sizePolicy().hasHeightForWidth())
        self.submit.setSizePolicy(sizePolicy)
        self.submit.setObjectName("submit")
        self.horizontalLayout_5.addWidget(self.submit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.reset = QtWidgets.QPushButton(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy)
        self.reset.setObjectName("reset")
        self.horizontalLayout_5.addWidget(self.reset)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_5.setStretch(0, 2)
        self.horizontalLayout_5.setStretch(2, 1)
        self.horizontalLayout_5.setStretch(4, 2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.list_res = QtWidgets.QListView(parent=self.widget)
        self.list_res.setObjectName("list_res")
        self.verticalLayout.addWidget(self.list_res)
        self.setWindowTitle("图像数据检索")
        self.start_label.setText("开始时间：")
        self.ip.setText("   IP地址：")
        self.user.setText("   用户名：")
        self.end_label.setText("结束时间：")
        self.submit.setText("开始检索")
        self.reset.setText("初始化")


        self.submit.clicked.connect(self.submit_fn)
        self.reset.clicked.connect(self.reset_fn)
        self.list_res.clicked.connect(self.listView_click)

    def show(self):
        self.exec()

    def load_qss(self,qss_file):
        with open(qss_file,'r') as file:
            qss_data = file.read()
        return qss_data

    def submit_fn(self):
        file_list = os.listdir(self.root_path+"resources/img/")
        starttime_dt = self.start_time.dateTime().toString("yyyyMMddHHmmss")
        endtime_dt = self.end_time.dateTime().toString("yyyyMMddHHmmss")
        target_user = self.user_edit.text()
        target_ip = self.ip_edit.text()
        res_list = list()
        for file in file_list:
            dt,user,ip = file.split("_")
            ip = ip[:ip.rfind(".")]
            if starttime_dt < dt < endtime_dt and (target_user == '' or target_user == user) and (target_ip == '' or target_ip == ip):
                res_list.append(file)
        fsm = QFileSystemModel()
        self.list_res.setModel(fsm)
        if len(res_list)>0:
            fsm.setRootPath(QDir.rootPath())
            fsm.setNameFilters(res_list)
            fsm.setNameFilterDisables(False)
            self.list_res.setRootIndex(fsm.index(self.root_path + "resources/img/"))
    def reset_fn(self):
        self.user_edit.setText("")
        self.ip_edit.setText("")
        self.start_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 1, 1), QtCore.QTime(0, 0, 0)))
        self.end_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2030, 1, 1), QtCore.QTime(0, 0, 0)))

    def listView_click(self,event):
        # 当前页面关闭
        self.close()
        # 第一个界面展示图片
        self.parent_page.tabWidget.setCurrentIndex(0)
        file = f"{self.root_path}resources/img/{event.data()}"
        self.cur_page.main_img.setPixmap(QPixmap(file))
        self.cur_page.cur_file.setText("选中文件："+file)
