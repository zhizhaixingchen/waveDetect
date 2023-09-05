# @Author      : Duhongkai
# @Time        : 2023/5/13 19:07
# @Description : 首页的动作

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import json
import os

def modify_action(action,line_edit):
    pass



def cancel_action(event):
    print(event)


def img_action(root_file):
    with open(f'{root_file}config/setting.jsonl', 'r') as f:
        settings = json.loads(f.read())
    # 获取默认设置
    img_widget = QDialog()
    img_widget.setWindowTitle('图像默认设置')
    img_widget.setWindowModality(Qt.WindowModality.ApplicationModal)  # 设置模态属性
    img_widget.setGeometry(300, 300, 700, 500)
    layout = QHBoxLayout()
    d_save_label = QLabel("图像默认保存路径：")
    d_save_lineEdit = QLineEdit()
    d_save_lineEdit.setEnabled(False)
    d_save_lineEdit.setText(settings["img"]["default_save_location"])
    d_save_button = QPushButton("修改")
    d_save_button.clicked.connect(lambda x: modify_action("img_default_save_location",d_save_lineEdit))

    layout.addWidget(d_save_label)
    layout.addWidget(d_save_lineEdit)
    layout.addWidget(d_save_button)
    img_widget.setLayout(layout)
    img_widget.exec()
    # 展示默认设置
    # 默认设置修改


def table_action(root_file):
    # 获取默认设置
    img_widget = QDialog()
    img_widget.setWindowModality(Qt.WindowModality.ApplicationModal)  # 设置模态属性
    img_widget.setGeometry(300, 300, 700, 500)
    layout = QFormLayout()
    row_label = QLabel("表格默认显示行数")
    row_lineEdit = QLineEdit()
    row_lineEdit.setText("5")
    row_label.setEnabled(False)

    confirm_button = QPushButton("确认")
    # confirm_button.clicked.connect(confirm_action)
    cancel_button = QPushButton("取消")
    # cancel_button.clicked.connect(cancel_action)

    layout.addRow(row_label, row_lineEdit)
    layout.addRow(confirm_button, cancel_button)
    img_widget.setLayout(layout)
    img_widget.exec()
    # 展示默认设置
    # 默认设置修改


def video_action():
    # 获取默认设置
    img_widget = QDialog()
    img_widget.setWindowModality(Qt.WindowModality.ApplicationModal)  # 设置模态属性
    img_widget.setGeometry(300, 300, 700, 500)
    layout = QFormLayout()
    row_label = QLabel("自动播放")
    radio_layout = QHBoxLayout()
    button_group = QButtonGroup()
    choice_A = QRadioButton('是')
    choice_A.setChecked(True)
    choice_B = QRadioButton('否')
    button_group.addButton(choice_A, 1)
    button_group.addButton(choice_B, 2)
    radio_layout.addWidget(choice_A)
    radio_layout.addWidget(choice_B)
    img_widget.setLayout(layout)

    confirm_button = QPushButton("确认")
    # confirm_button.clicked.connect(confirm_action)
    cancel_button = QPushButton("取消")
    # cancel_button.clicked.connect(cancel_action)

    layout.addRow(row_label,radio_layout)
    layout.addRow(confirm_button, cancel_button)
    img_widget.setLayout(layout)
    img_widget.exec()
    # 展示默认设置
    # 默认设置修改
