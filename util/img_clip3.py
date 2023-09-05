from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import cv2
import sys


class MyLabel(QLabel):
    def __init__(self,parent=None):
        super(MyLabel, self).__init__(parent)
        self.x0=0
        self.y0=0
        self.x1=0
        self.y1=0
        self.flag=False
        self.move=False     # 存在移动

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        # barHeight = self.bar.height()
        self.move = True
        if self.flag:
            self.x1 = event.pos().x()
            self.y1 = event.pos().y()
            self.update()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False
        self.move=False
        print(self.x0,self.y0,self.x1,self.y1)
        self.x0, self.y0, self.x1, self.y1=(0,0,0,0)
        print(self.x0, self.y0, self.x1, self.y1)

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        if self.flag and self.move:     # 只有当鼠标按下并且移动状态
            rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
            painter = QPainter(self)
            painter.setPen(QPen(Qt.GlobalColor.red, 2, Qt.SolidLine))
            painter.drawRect(rect)
        # print(self.x0, self.y0, self.x1, self.y1)


    # 单击鼠标触发事件
    def mousePressEvent(self, event):
        # barHeight = self.bar.height()
        self.x0 = event.pos().x()
        self.y0 = event.pos().y()
        self.flag = True


# 测试类
class Test(QWidget):
    def __init__(self):
        super(Test,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(960,540)
        self.setWindowTitle("在label中绘制矩形")
        self.label = MyLabel(self)          #重定义的label
        # self.label.setGeometry(QRect(30, 30, 511, 541))

        img = cv2.imread('dataSet/scene1380.jpg')
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.label.setPixmap(pixmap)
        self.label.setCursor(Qt.CrossCursor)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = Test()
    test.show()
    sys.exit(app.exec())


