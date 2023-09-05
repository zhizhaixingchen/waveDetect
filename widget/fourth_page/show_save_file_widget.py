# @Author      : Duhongkai
# @Time        : 2023/5/17 14:47
# @Description : 查看保存文件的widget
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QFileSystemModel, QPixmap
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListView

class Save_file_dialog(QDialog):
    def __init__(self,root_path,cur_page,parent_page):
        super().__init__()
        self.root_path = root_path
        self.parent_page = parent_page
        self.cur_page = cur_page
        self.show_save_file_widget()
        self.setStyleSheet(self.load_qss(self.root_path + 'static/qss/basic.qss'))


    def show_save_file_widget(self):
        layout = QVBoxLayout()
        self.setWindowTitle('存储文件列表')
        self.setWindowModality(Qt.WindowModality.ApplicationModal)  # 设置模态属性
        self.setGeometry(300, 300, 700, 500)
        fsm = QFileSystemModel()
        fsm.setRootPath(QDir.rootPath())
        lv = QListView()
        lv.setModel(fsm)
        lv.setRootIndex(fsm.index(self.root_path+"resources/img/"))
        layout.addWidget(lv)
        self.setLayout(layout)
        lv.clicked.connect(self.listView_click)

    def show(self):
        self.exec()

    def listView_click(self,event):
        # 当前页面关闭
        self.close()
        # 第一个界面展示图片
        self.parent_page.tabWidget.setCurrentIndex(0)
        file = f"{self.root_path}resources/img/{event.data()}"
        self.parent_page.first_page.main_img.setPixmap(QPixmap(file))
        self.parent_page.first_page.cur_file.setText("选中文件："+file)

    def load_qss(self,qss_file):
        with open(qss_file,'r') as file:
            qss_data = file.read()
        return qss_data