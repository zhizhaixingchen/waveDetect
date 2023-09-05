# @Author      : Duhongkai
# @Time        : 2023/5/22 13:39
# @Description : 自定义滑块
from PyQt6.QtCore import QEvent, Qt, pyqtSignal
from PyQt6.QtWidgets import QSlider, QApplication


class CustomSlider(QSlider):
    customPress = pyqtSignal()
    customRelease = pyqtSignal()
    def __init__(self, parent=None):
        super(CustomSlider, self).__init__(parent)

    def event(self, event):
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            self.customPress.emit()
        elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            self.customRelease.emit()
        return super().event(event)

    def initStyle(self):
        # 继承 QSlider 的样式
        self.setStyle(QApplication.style())
