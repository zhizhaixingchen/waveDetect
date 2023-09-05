# @Author      : Duhongkai
# @Time        : 2023/5/22 13:11
# @Description : 自定义滑块


from PyQt6.QtCore import Qt, QEvent, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QSlider, QVBoxLayout, QWidget

class CustomSlider(QSlider):
    customAction = pyqtSignal()
    def __init__(self):
        super().__init__()

    def event(self, event):
        if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
            print("aaa")
            self.customAction.emit()
        elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
            print("bbb")
            self.customAction.emit()
        return super().event(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建一个CustomSlider
        slider = CustomSlider()
        slider.setOrientation(Qt.Orientation.Horizontal)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(slider)

        # 创建一个主窗口
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
