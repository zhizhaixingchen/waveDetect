# @Author      : Duhongkai
# @Time        : 2023/5/18 12:48
# @Description : 自定义的QLabel

from PyQt6 import QtWidgets, QtCore
class Icon_QLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Icon_QLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.setStyleSheet("#reset_bn{border:2px outset #ddd}")
        self.button_clicked_signal.emit()

    def mousePressEvent(self, QMouseEvent):
        self.setStyleSheet("#reset_bn{border:2px inset #ddd}")

    # 可在外部与槽函数连接
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)
