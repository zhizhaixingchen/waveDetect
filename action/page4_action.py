# @Author      : Duhongkai
# @Time        : 2023/5/18 14:56
# @Description : 第四页action，大部分动作与第一页相似
import cv2
from PyQt6.QtGui import QImage, QPixmap, QFileSystemModel
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageFilter, ImageOps
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QDialog, QListView, QWidget, QVBoxLayout
import os
import datetime
import socket

from pymediainfo import MediaInfo

from fourth_page.show_save_file_widget import Save_file_dialog
from fourth_page.search_file_widget import Search_file_dialog
import sys

from imgPredict_Widget import Ui_ImgPredict
from ImgPredict_action import img_action,touch_action,stat_action

current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
import video_stream
import pic_frame_stream

global param
param = dict()
global video_decode_work
global video_play_work
global video_msg
global pic_frame
# 上方滑动窗口的action
def slide_action(signal):
    global param
    fourth_page, action, value, file_path, root_path = signal
    img = Image.open(f'{root_path}tmp/tmp.jpg')
    if action == 'bright':
        fourth_page.bright_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 5      # [0,10]
    elif action == 'clarity':
        fourth_page.clarity_per.setText(f"{value}%  ")
        value = value * 10
    elif action == 'exposure':
        fourth_page.exposure_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 10
    elif action == 'highlight':
        fourth_page.highlight_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 10
    elif action == 'contrast':
        fourth_page.contrast_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 10
    elif action == 'saturation':
        fourth_page.saturation_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 5
    elif action == 'sharpness':
        fourth_page.sharpness_per.setText(f"{value}%  ")
        if value==0:
            del param[action]
            qimage = modify_img(img)
            fourth_page.main_img.setPixmap(QPixmap(qimage))
            return
        else:
            value = value / 25
    elif action == 'temperature':
        fourth_page.temperature_per.setText(f"{value}%  ")
        value = -255 + 5.1 * value
    elif action == 'hue':  # highlight
        fourth_page.hue_per.setText(f"{value}%  ")
        value = -255 + 5.1 * value
    elif action == 'decolor':
        pass
    elif action == 'reverse':
        pass
    else:                  # 去噪方法 (denoise)
        pass
    param[action] = value
    qimage = modify_img(img)
    fourth_page.main_img.setPixmap(QPixmap(qimage))

# 左侧按钮action
def left_bn_action(signal):
    parent_page,fourth_page,action,root_path = signal
    if action == 'import':
        file,_ = QFileDialog.getOpenFileName(fourth_page, 'Open file', os.curdir, "Videos (*.mp4 *.avi *.mkv *.ogg)")
        if file != '':
            clear_globals()
            global video_msg,pic_frame
            mode = fourth_page.mode_combobox.currentText()
            video_msg = get_video_message(file)
            init_ui(fourth_page,file,root_path,mode)
            if mode == '视频流':
                # 初始化video线程，准备播放视频
                init_video_thread(file,fourth_page,root_path)
            # pic_frame不消耗空间，可以直接定义，方便后面使用
            pic_frame = pic_frame_stream.Pic_frame(fourth_page,file,video_msg)
    if action == 'export':
        default_file_name = fourth_page.cur_file.text().split("选中文件：")[1].split(".")[0]+".jpg"
        file,_ = QFileDialog.getSaveFileName(fourth_page, "save file", default_file_name,'Images (*.png *.jpg *.jpeg *.bmp *.gif)')
        if file != '':
            q_img = fourth_page.main_img.pixmap().toImage()
            q_img.save(file,file.split(".")[-1],100)
    if action == 'search':
        Search_file_dialog(root_path,fourth_page,parent_page).show()
    if action == 'show':
        Save_file_dialog(root_path,fourth_page,parent_page).show()
    if action == 'save':
        file_appendix = "jpg"
        file_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_" \
                    f"{socket.gethostname()}_" \
                    f"{socket.gethostbyname(socket.gethostname())}." \
                    f"{file_appendix}"
        q_img = fourth_page.main_img.pixmap().toImage()
        q_img.save(root_path+"resources/img/"+file_name, file_appendix, 100)
        QMessageBox.question(fourth_page, 'Message',"文件已保存。", QMessageBox.StandardButton.Yes)
    if action == 'predict':
        q_img = fourth_page.main_img.pixmap().toImage()
        new_cur_file = root_path + "tmp/tmp_predict.jpg"
        q_img.save(new_cur_file,'jpg', 100)
        img_predict = Ui_ImgPredict(root_path, new_cur_file)
        img_predict.btn_signal.connect(img_action)
        img_predict.touch_signal.connect(touch_action)
        img_predict.draw_signal.connect(stat_action)
        img_predict.show()

# 控制视频播放action
def video_bn_action(signal):
    global video_play_work,video_decode_work,video_msg,pic_frame
    fourth_page,widget_name,value,mode,cur_file,root_path = signal
    if 'video_play_work' not in globals():    # 第一次进入界面,对默认视频进行初始化
        video_msg = get_video_message(cur_file)
        init_ui(fourth_page,cur_file,root_path,mode)
        if mode == '视频流':
            init_video_thread(cur_file, fourth_page, root_path)
    if 'pic_frame' not in globals():
        pic_frame = pic_frame_stream.Pic_frame(fourth_page, cur_file, video_msg)
    if mode == '视频流':
        if widget_name == 'play_pause_btn':
            if video_play_work.playFlag:    # 暂停
                video_play_work.playFlag = False
                video_decode_work.threadFlag = False
                video_play_work.threadFlag = False
                img_setEnable(fourth_page,True)
                fourth_page.play_pause_btn.setPixmap(QPixmap(f"{root_path}static/img/video_play.png"))
                save_tmp_pic(mode,root_path)
            else:                           # 播放
                video_play_work.playFlag = True
                video_decode_work.threadFlag = True
                video_play_work.threadFlag = True
                video_decode_work.start()
                video_play_work.start()
                img_setEnable(fourth_page, False)
                fourth_page.play_pause_btn.setPixmap(QPixmap(f"{root_path}static/img/video_pause.png"))
                # 判断当前位置，如果是在开始位置并且decoder队列中没有元素，那么加载videoCapture
                if video_play_work.cur_frame_num == 0 and video_stream.Decode2Play.empty():
                    # video_decode_work.videoPath = cur_file      # 如果不添加这一行，video
                    video_decode_work.cap = cv2.VideoCapture(video_decode_work.videoPath)
        elif widget_name == 'slider_press':             # 在视频流中,slider不能仅由一个动作完成，应该是press和release配合完成
            video_play_work.threadFlag = False
            video_decode_work.threadFlag = False
            img_setEnable(fourth_page, False)
            fourth_page.play_pause_btn.setPixmap(QPixmap(f"{root_path}static/img/video_play.png"))
        elif widget_name == 'slider_release':
            frame = int(value * video_msg['frame_count'] / 100)
            modify_video_by_slider(fourth_page,frame,root_path)
        elif widget_name == 'pre_btn':
            video_play_work.threadFlag = False
            video_decode_work.threadFlag = False
            frame = max(video_play_work.cur_frame_num - value * video_msg['frame_rate'],0)
            modify_video_by_slider(fourth_page, frame, root_path)
        elif widget_name == 'next_btn':
            video_play_work.threadFlag = False
            video_decode_work.threadFlag = False
            frame = min(video_play_work.cur_frame_num + value * video_msg['frame_rate'],video_msg['frame_count'])
            modify_video_by_slider(fourth_page, frame, root_path)
        elif widget_name == 'mode_combobox':
            mode_switch(fourth_page,mode,root_path,cur_file)
    else:            # 图片帧不再使用多线程
        if widget_name in 'slider_release':
            value = int(value * video_msg['frame_count'] / 100)
            pic_frame.get_frame(value)
            save_tmp_pic(mode, root_path)
            fourth_page.reset_png()
        elif widget_name == 'pre_btn':
            pic_frame.pre_frame()
            save_tmp_pic(mode, root_path)
            fourth_page.reset_png()
        elif widget_name == 'next_btn':
            pic_frame.next_frame()
            save_tmp_pic(mode, root_path)
            fourth_page.reset_png()
        elif widget_name == "mode_combobox":    # 该部分代码和视频流中代码一致，为了便于理解，代码冗余
            mode_switch(fourth_page,mode,root_path,cur_file)
            if 'video_play_work' in globals() and video_play_work.frame is not None:
                save_tmp_pic("视频流",root_path)   # 切换后，保存视频流最后一帧






def pil2qimage(pil_image):
    width, height = pil_image.size
    pil_image = pil_image.convert("RGBA")
    image = QImage(pil_image.tobytes(), width, height, QImage.Format.Format_RGBA8888)
    return image

def modify_img(img):
    global param
    if 'bright' in param:
        brightEnhancer = ImageEnhance.Brightness(img)
        img = brightEnhancer.enhance(param['bright'])
    if 'clarity' in param:
        img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=param['clarity']))
    if 'exposure' in param:
        img = np.array(img)
        adjusted_image = img * param['exposure']
        adjusted_image = np.clip(adjusted_image, 0, 255)
        img = adjusted_image.astype(np.uint8)
        img = Image.fromarray(img)
    if 'highlight' in param:
        enhancer = ImageEnhance.Contrast(img)
        highlight_adjusted = enhancer.enhance(param['highlight'])
        enhancer = ImageEnhance.Brightness(highlight_adjusted)
        img = enhancer.enhance(param['highlight'])
    if 'contrast' in param:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(param['contrast'])
    if 'saturation' in param:
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(param['saturation'])
    if 'sharpness' in param:
        kernel = [
            -1, -1, -1,
            -1, 12-param['sharpness'], -1,
            -1, -1, -1
        ]
        sharpen_filter = ImageFilter.Kernel(size=(3,3), kernel=kernel)
        img = img.filter(sharpen_filter)
    if 'temperature' in param:
        # 计算蓝色和黄色的增益值
        temp = param['temperature']
        if temp > 0:
            r, g, b = 255, 255 - temp, 255 - temp
        else:
            r, g, b = 255 + temp, 255 + temp, 255
        # 调整图像的色温
        temp_img = ImageOps.colorize(img.convert('L'), (r, g, b), (255, 255, 255))
        img_data = np.array((np.array(img) + np.array(temp_img)) - 255).astype(np.uint8)
        img = Image.fromarray(img_data)
    if 'hue' in param:
        image_hsv = img.convert('HSV')
        hue, saturation, value = image_hsv.split()
        hue = hue.point(lambda h: (h + param['hue']) % 256)
        image_hsv = Image.merge('HSV', (hue, saturation, value))
        img = image_hsv.convert('RGB')
    if 'decolor' in param and param['decolor']:
        img = img.convert('L')
    if 'reverse' in param and param['reverse']:
        img = ImageOps.invert(img)
    if 'denoise' in param:
        if param['denoise'] == '锐化滤波':
            img = img.filter(ImageFilter.SHARPEN)
        if param['denoise'] == '模糊滤波':
            img = img.filter(ImageFilter.BLUR)
        if param['denoise'] == '轮廓滤波':
            img = img.filter(ImageFilter.CONTOUR)
        if param['denoise'] == '浮雕滤波':
            img = img.filter(ImageFilter.EMBOSS)
        if param['denoise'] == '细节增强滤波':
            img = img.filter(ImageFilter.DETAIL)
        if param['denoise'] == '边缘增强滤波':
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        if param['denoise'] == '深度边缘增强滤波':
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        if param['denoise'] == '寻找边缘信息滤波':
            img = img.filter(ImageFilter.FIND_EDGES)
        if param['denoise'] == '平滑滤波':
            img = img.filter(ImageFilter.SMOOTH)
        if param['denoise'] == '深度平滑滤波':
            img = img.filter(ImageFilter.SMOOTH_MORE)
    return pil2qimage(img)

def init_video_thread(file,fourth_page,root_path):
    global video_decode_work,video_play_work,video_msg
    video_decode_work = video_stream.cvDecode(file)
    video_decode_work.start()
    video_play_work = video_stream.playVedio(fourth_page,video_msg,root_path)
    video_play_work.start()

def get_video_message(file):
    media_info = MediaInfo.parse(file)
    duration = int(int(media_info.to_data()['tracks'][1]['duration'])/1000)
    width = int(media_info.to_data()['tracks'][1]['width'])
    height = int(media_info.to_data()['tracks'][1]['height'])
    frame_rate = float(media_info.to_data()['tracks'][1]['frame_rate'])
    frame_count = int(media_info.to_data()['tracks'][1]['frame_count'])
    stream_size = int(media_info.to_data()['tracks'][1]['stream_size'])     # 文件大小？b
    return {"duration":duration,"width":width,"height":height,"frame_rate":frame_rate,"frame_count":frame_count,"stream_size":stream_size}

def init_ui(fourth_page,file,root_path,mode):
    global video_msg
    if mode == '视频流':
        minute, second = divmod(video_msg['duration'], 60)
        fourth_page.video_time.setText(f"0:00/{minute}:{'{:02}'.format(second)}")
    else:   # 图片帧
        fourth_page.video_time.setText(f"0/{video_msg['frame_count']}")
    fourth_page.video_slider.setValue(0)
    fourth_page.cur_file.setText("选中文件：" + file)
    img_setEnable(fourth_page, True)
    fourth_page.play_pause_btn.setPixmap(QPixmap(f"{root_path}static/img/video_play.png"))
    # 获取第一帧
    frame = cv2.VideoCapture(file).read()[1]
    # image = cv2.resize(frame, (400, 320))
    image = frame
    qImg = QImage(image, image.shape[1], image.shape[0], QImage.Format.Format_RGB888).rgbSwapped()
    fourth_page.main_img.setPixmap(QPixmap.fromImage(qImg))

def clear_globals():
    global video_decode_work,video_play_work,video_msg
    video_stream.Decode2Play.queue.clear()
    if 'video_decode_work' in globals():
        video_decode_work.threadFlag = False
        # del video_decode_work
    if 'video_play_work' in globals():
        video_play_work.threadFlag = False
        # del video_play_work

# 释放就开始播放视频
def modify_video_by_slider(fourth_page,frame,root_path):
    global video_play_work, video_decode_work, video_msg
    video_play_work.playFlag = True
    img_setEnable(fourth_page, False)
    fourth_page.play_pause_btn.setPixmap(QPixmap(f"{root_path}static/img/video_pause.png"))
    video_stream.Decode2Play.queue.clear()
    video_decode_work.cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
    video_decode_work.threadFlag = True
    video_decode_work.start()

    video_play_work.threadFlag = True
    video_play_work.cur_frame_num = frame
    video_play_work.start()
    # fourth_page.video_slider.setValue(frame / video_msg['frame_count'] * 100)
    # video_play_work.cur_frame_num = max(value - 1,0)


# 中途修改模式
def mode_switch(fourth_page,cur_mode,root_path,video_file):
    global video_msg,video_play_work,video_decode_work,pic_frame
    if cur_mode == "视频流":
        used_minute, used_second = divmod(int(pic_frame.cur_frame_index / video_msg['frame_rate']),                                  60)
        total_minute, total_second = divmod(video_msg['duration'], 60)
        fourth_page.video_time.setText(
            f"{used_minute}:{'{:02}'.format(used_second)}/{total_minute}:{'{:02}'.format(total_second)}")
        fourth_page.play_pause_btn.setEnabled(True)
        img_setEnable(fourth_page, True)
        fourth_page.play_pause_btn.setPixmap(QPixmap(f"{root_path}static/img/video_play.png"))
        # fourth_page.video_slider.setValue(video_play_work.cur_frame_num / video_msg['frame_count'] * 100)
        # 视频流开始工作
        clear_globals()
        video_decode_work = video_stream.cvDecode(video_file)
        video_decode_work.cap.set(cv2.CAP_PROP_POS_FRAMES, pic_frame.cur_frame_index+1)
        video_play_work = video_stream.playVedio(fourth_page, video_msg, root_path)
        video_play_work.cur_frame_num = pic_frame.cur_frame_index
        video_play_work.playFlag = False
        video_decode_work.threadFlag = False
        video_play_work.threadFlag = False
    else:
        if 'video_decode_work' in globals():
            video_decode_work.threadFlag = False
            video_play_work.threadFlag = False
            video_play_work.playFlag = False
            # 更新图片帧索引
            pic_frame.cur_frame_index = int(video_play_work.cur_frame_num)
        fourth_page.video_time.setText(f"{pic_frame.cur_frame_index}/{video_msg['frame_count']}")
        fourth_page.play_pause_btn.setEnabled(False)
        img_setEnable(fourth_page, True)
        fourth_page.play_pause_btn.setPixmap(QPixmap(f"{root_path}static/img/video_play_disable.png"))


def save_tmp_pic(mode,root_path):
    global video_play_work,pic_frame
    if mode == "视频流":
        cv2.imwrite(f"{root_path}tmp/tmp.jpg",video_play_work.frame)
    else:
        cv2.imwrite(f"{root_path}tmp/tmp.jpg",pic_frame.frame)

# 禁用/启用调节按钮
def img_setEnable(fourth_page,enable):
    fourth_page.bright_slider.setEnabled(enable)
    fourth_page.clarity_slider.setEnabled(enable)
    fourth_page.exposure_slider.setEnabled(enable)
    fourth_page.highlight_slider.setEnabled(enable)
    fourth_page.contrast_slider.setEnabled(enable)
    fourth_page.saturation_slider.setEnabled(enable)
    fourth_page.sharpness_slider.setEnabled(enable)
    fourth_page.temperature_slider.setEnabled(enable)
    fourth_page.hue_slider.setEnabled(enable)
    fourth_page.denoise_combobox.setEnabled(enable)
    fourth_page.decolor.setEnabled(enable)
    fourth_page.reverse.setEnabled(enable)
    fourth_page.reset_bn.setEnabled(enable)
    if not enable:
        fourth_page.reset_png()
