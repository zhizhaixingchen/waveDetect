# @Author      : Duhongkai
# @Time        : 2023/5/22 16:20
# @Description : 图片裁剪
# 绘制事件

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QImage, QPainter, QColor, QPen, QPixmap
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drawing Example")
        self.setGeometry(100, 100, 400, 300)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 400, 300)

        self.image = QImage(400, 300, QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)

        self.draw_rectangle()

    def draw_rectangle(self):
        painter = QPainter(self.image)
        painter.setPen(QPen(QColor(255, 0, 0), 2))  # 设置画笔颜色和宽度
        painter.drawRect(50, 50, 200, 150)  # 绘制矩形
        painter.end()

        self.label.setPixmap(QPixmap.fromImage(self.image))

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

"""
plotdigitizer figures/graphs_1.png -p 1,0 -p 6,0 -p 0,3 -l 165,160 -l 599,160 -l 85,60 --plot figures/graphs_1.result.png --preprocess
plotdigitizer  figures/ECGImage.png -p 1,0 -p 5,0 -p 0,1 -l 290,337 -l 1306,338 -l 106,83 --plot figures/ECGImage.result.png
plotdigitizer  figures/test.jpg -p 0,0 -p 5,0 -p 5,4 -p 5,-4 --plot figures/test_result.jpg
"""

