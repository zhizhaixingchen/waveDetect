# @Author      : Duhongkai
# @Time        : 2023/5/22 20:51
# @Description :

from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6.QtCore import Qt

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            print("左键点击")
        elif event.button() == Qt.MouseButton.RightButton:
            print("右键点击")

if __name__ == '__main__':
    app = QApplication([])
    dialog = MyDialog()
    dialog.show()
    app.exec()