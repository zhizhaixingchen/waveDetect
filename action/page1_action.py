# @Author      : Duhongkai
# @Time        : 2023/5/16 9:28
# @Description : 第一个界面的action
from PyQt6.QtCore import Qt, QDir
from PyQt6.QtGui import QImage, QPixmap
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
import datetime
import socket
from first_page.show_save_file_widget import Save_file_dialog
from first_page.search_file_widget import Search_file_dialog
from imgPredict_Widget import Ui_ImgPredict
from ImgPredict_action import img_action,touch_action,stat_action
from mouse_click import MyDialog

global param
param = dict()
# 上方滑动窗口的action
def slide_action(signal):
    global param
    first_page, action, value, file_path = signal
    img = Image.open(file_path)
    if action == 'bright':
        first_page.bright_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 5      # [0,10]
    elif action == 'clarity':
        first_page.clarity_per.setText(f"{value}%  ")
        value = value * 10
    elif action == 'exposure':
        first_page.exposure_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 10
    elif action == 'highlight':
        first_page.highlight_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 10
    elif action == 'contrast':
        first_page.contrast_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 10
    elif action == 'saturation':
        first_page.saturation_per.setText(f"{value}%  ")
        value = value / 50 if value < 50 else 1 + (value - 50) / 5
    elif action == 'sharpness':
        first_page.sharpness_per.setText(f"{value}%  ")
        if value==0:
            del param[action]
            qimage = modify_img(img)
            first_page.main_img.setPixmap(QPixmap(qimage))
            return
        else:
            value = value / 25
    elif action == 'temperature':
        first_page.temperature_per.setText(f"{value}%  ")
        value = -255 + 5.1 * value
    elif action == 'hue':  # highlight
        first_page.hue_per.setText(f"{value}%  ")
        value = -255 + 5.1 * value
    elif action == 'decolor':
        pass
    elif action == 'reverse':
        pass
    else:                  # 去噪方法 (denoise)
        pass
    param[action] = value
    qimage = modify_img(img)
    first_page.main_img.setPixmap(QPixmap(qimage))

# 左侧按钮action
def left_bn_action(signal):
    first_page,action,root_file = signal
    if action == 'import':
        file,_ = QFileDialog.getOpenFileName(first_page, 'Open file', os.curdir, "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file != '':
            first_page.main_img.setPixmap(QPixmap(file))
            first_page.cur_file.setText("选中文件："+file)
    if action == 'export':
        default_file_name = first_page.cur_file.text().split("选中文件：")[1]
        file,_ = QFileDialog.getSaveFileName(first_page, "save file", default_file_name,'Images (*.png *.jpg *.jpeg *.bmp *.gif)')
        if file != '':
            q_img = first_page.main_img.pixmap().toImage()
            q_img.save(file,file.split(".")[-1],100)
    if action == 'search':
        Search_file_dialog(root_file,first_page).show()
    if action == 'show':
        Save_file_dialog(root_file,first_page).show()
    if action == 'save':
        file_appendix = first_page.cur_file.text().split("选中文件：")[1].split(".")[1]
        file_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_" \
                    f"{socket.gethostname()}_" \
                    f"{socket.gethostbyname(socket.gethostname())}." \
                    f"{file_appendix}"
        q_img = first_page.main_img.pixmap().toImage()
        q_img.save(root_file+"resources/img/"+file_name, file_appendix, 100)
        QMessageBox.question(first_page, 'Message',"文件已保存。", QMessageBox.StandardButton.Yes)
    if action == 'predict':
        q_img = first_page.main_img.pixmap().toImage()
        new_cur_file = root_file + "tmp/tmp_predict.jpg"
        q_img.save(new_cur_file,'jpg', 100)
        img_predict = Ui_ImgPredict(root_file,new_cur_file)
        img_predict.btn_signal.connect(img_action)
        img_predict.touch_signal.connect(touch_action)
        img_predict.draw_signal.connect(stat_action)
        img_predict.show()



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
