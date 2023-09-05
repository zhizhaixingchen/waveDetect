# @Author      : Duhongkai
# @Time        : 2023/5/20 17:47
# @Description : 展示某一帧图片

import cv2
input_video_path = 'D:/203demo/resources/default_video.mp4'
output_img_path = 'C:/Users/Never/Desktop/tmp.jpg'
cap = cv2.VideoCapture(input_video_path)
frame = 0
cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
ret, frame = cap.read()
cv2.imwrite(output_img_path,frame)
cap.release()