import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QLabel(self)
        self.label.setText("111111111111111111")
        self.label.setGeometry(50, 50, 200, 200)
        self.label.setMouseTracking(True)
        self.setCentralWidget(self.label)

        self.points = []  # 保存点击位置的点坐标

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.label.underMouse():
            pos = event.pos() - self.label.pos()  # 转换为相对于label的坐标
            self.points.append(pos)  # 将点击位置添加到点列表中
            self.updateLabel()  # 更新label的绘制

    def paintEvent(self, event):
        painter = QPainter(self.label)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.black)
        painter.setBrush(Qt.black)

        for point in self.points:
            painter.drawEllipse(point, 5, 5)  # 在点击位置绘制一个半径为5的圆

    def updateLabel(self):
        self.label.update()

    def closeEvent(self, event):
        # 关闭窗口时清空点列表
        self.points = []
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
