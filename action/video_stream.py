# @Author      : Duhongkai
# @Time        : 2023/5/18 19:39
# @Description : opencv+pyQT+多线程
"""
cv.VideoCapture(摄像头信息(文件信息))                    打开摄像头，并完成初始化工作
cv.VideoCapture(摄像头信息(文件信息)).isOpened()         判断摄像头是否打开
cv2.VideoCapture.open()                               如果打开失败，可以使用该方法尝试打开，
result=cv2.VideoCapture.open(filename)                尝试打开文件
cv2.VideoCapture.read()                               获取捕获帧信息(图片)
cv2.VideoCapture.release()                            关闭摄像头
"""
import time
from PyQt6.QtCore import QThread
from PyQt6.QtGui import *
import cv2
from queue import Queue
from pymediainfo import MediaInfo

Decode2Play = Queue()
class cvDecode(QThread):  # 视频解码
    def __init__(self,videoPath):
        super(cvDecode, self).__init__()
        self.threadFlag = True          # 线程状态
        self.videoPath = videoPath      # 视频文件路径path
        self.changeFlag = False         # 判断视频文件路径是否更改
        self.isCycle = False            # 是否循环播放
        self.cap = cv2.VideoCapture(videoPath)
        self.cap.set(cv2.CAP_PROP_POS_FRAMES,2)

    def run(self):
        while self.threadFlag:  # 线程开启状态
            # if self.changeFlag == True and self.videoPath !="":        # 改变视频文件
            #     self.changeFlag = False
            #     self.cap = cv.VideoCapture(r""+self.videoPath)
            # if self.videoPath != "":
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if frame is None and self.isCycle:  # 控制循环播放
                    self.cap = cv2.VideoCapture(r"" + self.videoPath)
                if ret:
                    # print(ret)
                    Decode2Play.put(frame)  # 解码后的数据放到队列中
                del frame  # 释放资源
            else:
                #   控制重连
                self.cap = cv2.VideoCapture(r"" + self.videoPath)
            if Decode2Play.qsize() > 300:   # 防止长视频，爆内存
                time.sleep(0.2)
            else:
                time.sleep(0.01)


class playVedio(QThread):  # 视频播放类
    def __init__(self,fourth_page,video_msg,root_path):
        super(playVedio, self).__init__()
        self.video_msg = video_msg
        self.fourth_page = fourth_page
        self.threadFlag = True              # 控制线程退出
        self.playFlag = False               # 控制播放/暂停标识，默认暂停
        self.cur_frame_num = 0              # 当前帧数
        self.root_path = root_path
        self.frame = None

    def run(self):
        while self.threadFlag:  # 线程开启状态
            if self.playFlag and not Decode2Play.empty():  # 当前状态播放
                self.frame = Decode2Play.get()  # 从队列中读取视频帧
                # image = cv2.resize(self.frame, (400, 320))  # 调整为显示尺寸
                image = self.frame
                self.fourth_page.video_slider.setValue(self.cur_frame_num/self.video_msg['frame_count']*100)
                used_minute,used_second = divmod(int(self.cur_frame_num/self.video_msg['frame_rate']),60)
                total_minute,total_second = divmod(self.video_msg['duration'],60)
                self.fourth_page.video_time.setText(f"{used_minute}:{'{:02}'.format(used_second)}/{total_minute}:{'{:02}'.format(total_second)}")
                # RGB-BGR(交换)
                qImg = QImage(image, image.shape[1], image.shape[0], QImage.Format.Format_RGB888).rgbSwapped()
                time.sleep(0.015)
                self.fourth_page.main_img.setPixmap(QPixmap.fromImage(qImg))   #   图像在QLabel上展示
                self.cur_frame_num += 1
            # 当前视频播放完毕，按钮和当前帧数和slider\text初始化
            if self.cur_frame_num == self.video_msg['frame_count']:
                self.cur_frame_num = 0
                self.playFlag = False
                self.fourth_page.video_slider.setValue(0)
                minute, second = divmod(self.video_msg['duration'], 60)
                self.fourth_page.video_time.setText(f"0:00/{minute}:{second}")
                self.fourth_page.play_pause_btn.setPixmap(QPixmap(f"{self.root_path}static/img/video_play.png"))



# class video_action():  # 继承 QMainWindow 类和 Ui_MainWindow 界面类
#     def __init__(self, parent=None):
#         super(MyMainWindow, self).__init__(parent)  # 初始化父类
#
#     def openVideo(self):  # 导入视频文件，点击 btn_1 触发
#         if self.btn_1.text() == "打开视频":
#             # 打开视频文件
#             self.videoPath, _ = QFileDialog.getOpenFileName(self, "Open Video", "../images/", "*.mp4 *.avi *.mov")
#             print("Open Video: ", self.videoPath)
#
#             # 实例化 cvDecode 类
#             self.decodework = cvDecode()
#             self.decodework.start()
#             self.decodework.threadFlag = True
#             self.decodework.changeFlag = True
#             self.decodework.videoPath = r"" + self.videoPath
#
#             # 实例化 playVideo 类
#             self.playwork = playVedio()
#             self.playwork.playLabel = self.label_1  # 设置显示控件 label_1
#             self.playwork.threadFlag = True
#             self.playwork.playFlag = True           # 控制标识：播放
#
#             # 创建视频播放线程
#             self.playthread = QThread()
#             self.playwork.moveToThread(self.playthread)
#             self.playthread.started.connect(self.playwork.play)  # 线程与类方法进行绑定
#             self.playthread.start()  # 启动视频播放线程
#
#             # 视频/摄像头，准备播放
#             self.btn_1.setText("关闭视频")
#             self.btn_2.setEnabled(True)  # "播放"按钮 可用
#             self.btn_3.setEnabled(True)  # "抓拍"按钮 可用
#         else:
#             self.closeEvent(self.close)  # 关闭线程
#             self.btn_1.setText("打开视频")
#             self.btn_2.setText("播放视频")
#             self.btn_2.setEnabled(False)  # "播放"按钮 不可用
#             self.btn_3.setEnabled(False)  # "抓拍"按钮 不可用
#
#     def playPause(self):  # 暂停/播放控制，点击 btn_2 触发
#         if self.btn_2.text() == "暂停播放":
#             self.playwork.playFlag = False  # 控制标识：暂停
#             self.btn_2.setText("播放视频")
#         else:
#             self.btn_2.setText("暂停播放")
#             self.playwork.playFlag = True  # 控制标识：播放
#
#     def captureFrame(self):  # 抓拍视频图像，点击 btn_3 触发
#         wLabel, hLabel = 400, 320
#         self.image = cv.resize(self.playwork.frame, (wLabel, hLabel))  # 调整为显示尺寸
#         qImg = QImage(self.image, wLabel, hLabel, QImage.Format_RGB888).rgbSwapped()  # OpenCV 转为 PyQt 图像格式
#         self.label_2.setPixmap((QPixmap.fromImage(qImg)))  # 加载 PyQt 图像
#         self.btn_4.setEnabled(True)  # "处理"按钮 可用
#
#     def imageProcess(self):  # 抓拍视频图像，点击 btn_4 触发
#         gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)  # 转为灰度图像
#         row, col, pix = gray.shape[0], gray.shape[1], gray.strides[0]
#         qImg = QImage(gray.data, col, row, pix, QImage.Format_Indexed8)
#         # qImg = QImage(self.image, row, col, QImage.Format_RGB888)  # OpenCV 转为 PyQt 图像格式
#         self.label_2.setPixmap((QPixmap.fromImage(qImg)))  # 加载 PyQt 图像
#
#     def closeEvent(self, event):  # 关闭线程
#         print("关闭线程")  # 先退出循环才能关闭线程
#         if self.decodework.isRunning():  # 关闭解码
#             self.decodework.threadFlag = False
#             self.decodework.quit()
#         if self.playthread.isRunning():  # 关闭播放线程
#             self.playwork.threadFlag = False
#             self.playthread.quit()
#
#     def refreshShow(self, img, label):  # 刷新显示图像
#         qImg = self.cvToQImage(img)  # OpenCV 转为 PyQt 图像格式
#         label.setPixmap((QPixmap.fromImage(qImg)))  # 加载 PyQt 图像
#         return
#
#     def trigger_actHelp(self):  # 动作 actHelp 触发
#         QMessageBox.about(self, "About",
#                           """多线程视频播放器 v1.0\nCopyright YouCans, XUPT 2023""")
#         return

