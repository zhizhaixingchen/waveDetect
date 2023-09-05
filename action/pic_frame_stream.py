# @Author      : Duhongkai
# @Time        : 2023/5/20 14:47
# @Description : 图片帧处理

import cv2
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QMessageBox


class Pic_frame():
    def __init__(self,fourth_page,videoPath,video_msg):
        self.fourth_page = fourth_page
        self.videoPath = videoPath
        self.cap = cv2.VideoCapture(videoPath)
        self.video_msg = video_msg
        self.cur_frame_index = 0
        self.frame = None

    def next_frame(self):
        if self.cur_frame_index == self.video_msg['frame_count']-1:
            QMessageBox.question(self.fourth_page, 'Message', "当前帧是最后一帧", QMessageBox.StandardButton.Yes)
        else:
            self.get_frame(self.cur_frame_index+1)

    def pre_frame(self):
        if self.cur_frame_index == 0:
            QMessageBox.question(self.fourth_page, 'Message', "当前帧是第一帧", QMessageBox.StandardButton.Yes)
        else:
            self.get_frame(self.cur_frame_index-1)

    def get_frame(self,index):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret,self.frame = self.cap.read()
        if ret:
            # image = cv2.resize(frame, (400, 320))
            image = self.frame
            self.fourth_page.video_slider.setValue(index/self.video_msg['frame_count'] * 100)
            self.fourth_page.video_time.setText(f"{index}/{self.video_msg['frame_count']}")
            qImg = QImage(image, image.shape[1], image.shape[0], QImage.Format.Format_RGB888).rgbSwapped()
            self.fourth_page.main_img.setPixmap(QPixmap.fromImage(qImg))
            self.cur_frame_index = index
        else:
            QMessageBox.question(self.fourth_page, 'Message', "获取失败，请重试。", QMessageBox.StandardButton.Yes)
