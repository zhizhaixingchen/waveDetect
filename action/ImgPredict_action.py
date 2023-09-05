# @Author      : Duhongkai
# @Time        : 2023/5/22 20:00
# @Description : 图片预测action
import os
import time
import cv2
# 针对图像的操作
# 图像保存
from PIL import Image,ImageQt, ImageDraw
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QImage, QPixmap
import numpy as np
from PyQt6.QtWidgets import QMessageBox, QFileDialog
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')
plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"] = False #该语句解决图像中的“-”负号的乱码问题



img_width = 600
img_height = 450

def img_action(signal):
    pred_page, obj_name,mode, root_path, cur_file = signal
    if obj_name == 'img_clip_btn':      # 图像裁剪
        if pred_page.lt_edit.text() and pred_page.rb_edit.text():
            lt_pointer = [int(i) for i in pred_page.lt_edit.text()[1:-1].split(",")]
            rb_pointer = [int(i) for i in pred_page.rb_edit.text()[1:-1].split(",")]
            # 将点标准化为左上角和右下角点
            lt_pointer[0],lt_pointer[1],rb_pointer[0],rb_pointer[1] = min(lt_pointer[0],rb_pointer[0]),min(lt_pointer[1],rb_pointer[1]),max(lt_pointer[0],rb_pointer[0]),max(lt_pointer[1],rb_pointer[1])
            if rb_pointer[0] - lt_pointer[0] != 0 and rb_pointer[1] - lt_pointer[1] != 0:   # 保证有意义
                raw_img = pred_page.clip_img_old
                raw_img = raw_img.scaled(img_width,img_height)
                img = ImageQt.fromqimage(raw_img)

                imgCrop = img.crop(lt_pointer + rb_pointer)
                qImg_old = ImageQt.toqimage(imgCrop)
                qImg_old = qImg_old.scaled(img_width,img_height)
                pred_page.clip_img_old = qImg_old

                draw = ImageDraw.Draw(img)
                draw.rectangle(lt_pointer + rb_pointer,outline='red',width=2)
                imgCrop = img.crop(lt_pointer + rb_pointer)
                qImg = ImageQt.toqimage(imgCrop)
                qImg = qImg.scaled(img_width, img_height)
                pred_page.clip_img = qImg

                pred_page.raw_img.setPixmap(QPixmap.fromImage(qImg))
                pred_page.start_pos = None
                pred_page.end_pos = None
                pred_page.mask_img = None
                pred_page.lt_edit.setText("")
                pred_page.rb_edit.setText("")
    elif obj_name == 'img_reset_btn':       # 撤销裁剪
        reset_img(pred_page,cur_file)
    elif obj_name == 'img_auto_btn':   # 图像边框自动识别
        pred_page.mask_img = None
        auto_mode(pred_page)
    elif obj_name == 'stat_reset_btn':  # 操作重置
        pred_page.mask_img = None
        current_img = qimg2cv(pred_page.clip_img_old)
        refresh_img(pred_page,current_img)
    elif obj_name == 'img_import_btn':
        file,_ = QFileDialog.getOpenFileName(pred_page, 'Open file', os.curdir, "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file != '':
            pred_page.cur_file = file
            reset_img(pred_page,file)

def touch_action(signal):
    pred_page,click_pos,touch_mode = signal
    if touch_mode == 'img_picker_btn':
        # 检查拾色器面积是不是过小
        if check_area(pred_page):
            color_set = pos2color(pred_page,click_pos)
            pick_color(pred_page,color_set)
    elif touch_mode == 'img_earse_btn':
        earse_color(pred_page,click_pos,int(pred_page.earse_size_label.text()))
    elif touch_mode == 'color_pre_btn':
        if check_area(pred_page):
            pick_color(pred_page,click_pos)

def reset_img(pred_page,cur_file):
    pred_page.clip_img_old = QImage(f"{cur_file}")
    pred_page.clip_img_old = pred_page.clip_img_old.scaled(600, 450)
    pred_page.clip_img = pred_page.clip_img_old
    pred_page.raw_img.setPixmap(QPixmap.fromImage(pred_page.clip_img))
    pred_page.lt_edit.setText("")
    pred_page.rb_edit.setText("")
    pred_page.start_pos = None
    pred_page.end_pos = None
    pred_page.mask_img = None

# 折线图预览、下载等
def stat_action(signal):

    pred_page,obj_name = signal
    if obj_name == 'img_pre_btn':
        color_extractor(pred_page)
        # 可以保存图片啦
        pred_page.img_save_btn.setEnabled(True)
    elif obj_name == 'img_save_btn':
        dialog = QFileDialog(pred_page)
        dialog.setWindowTitle("请选择保存路径")
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            file = dialog.selectedFiles()[0]
            if file != "":
                if os.path.isfile(file):
                    file = os.path.dirname(file)
                if pred_page.save_mode.currentText() == '保存图像和折线图':
                    pred_page.raw_img.pixmap().toImage().save(f"{file}/{int(time.time())}_left.jpg")
                    pred_page.stat_graph.print_figure(f"{file}/{int(time.time())}_right.jpg",dpi=300)
                elif pred_page.save_mode.currentText() == '仅保存折线图':
                    pred_page.stat_graph.print_figure(f"{file}/{int(time.time())}_right.jpg",dpi=300)
                elif pred_page.save_mode.currentText() == '仅保存图像':
                    pred_page.raw_img.pixmap().toImage().save(f"{file}/{int(time.time())}_left.jpg")
                else:   # 保存点迹数据
                    for key,value in pred_page.dot_dict.items():
                        np.savetxt(f'{file}/{int(time.time())}_{key}.csv', value[1], delimiter=",",fmt="%.4f")


def auto_mode(pred_page):
    raw_img = pred_page.clip_img_old
    current_img = qimg2cv(raw_img)
    res = find_box(current_img)
    if res:
        [x, y, w, h] = res
        box_x1 = x
        box_x2 = x+w
        box_y1 = y
        box_y2 = y+h
        # pos_left_bottom = [box_x1,box_y2]
        # pos_right_top = [box_x2,box_y1]
        # 更新坐标
        pred_page.lt_edit.setText(f"({box_x1},{box_y1})")
        pred_page.rb_edit.setText(f"({box_x2},{box_y2})")
        pred_page.start_pos = QPoint(box_x1,box_y1)
        pred_page.end_pos = QPoint(box_x2,box_y2)
        refresh_img(pred_page,current_img)

# 自动监测算法
def find_box(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,51,9)
    # Fill rectangular contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, (255,255,255), -1)
    # Morph open
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=4)
    # Draw rectangles
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        # cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 1)
        return [x+1,y+1,w-2,h-2]

def refresh_img(pred_page,current_img):
    height, width, _ = current_img.shape
    img_to_show = current_img.copy()
    # 将mask_img添加到图片上
    if pred_page.mask_img is not None:
        if(pred_page.mask_img.ndim==2):
            if pred_page.start_pos:
                bool_mask = np.zeros_like(pred_page.mask_img, dtype=bool)
                bool_mask[pred_page.start_pos.y():pred_page.end_pos.y(),pred_page.start_pos.x():pred_page.end_pos.x()] = True
                pred_page.mask_img[~bool_mask] = 0
            show_mask = np.tile(pred_page.mask_img[:,:,np.newaxis],3)
        else:
            show_mask = pred_page.mask_img
        # Morph with mask
        img_to_show=cv2.addWeighted(img_to_show,0.5,show_mask,1,0)
    # 将框添加到图片上
    if pred_page.start_pos:
        # x1 = pos_left_bottom[0]
        # y1 = pos_right_top[1]
        # x2 = pos_right_top[0]
        # y2 = pos_left_bottom[1]
        cv2.rectangle(img_to_show, (pred_page.start_pos.x(), pred_page.start_pos.y()), (pred_page.end_pos.x(), pred_page.end_pos.y()), (0,0,255), 1)        # BGR
    # 展示
    qImg = QImage(img_to_show.tobytes(), width, height, 3 * width, QImage.Format.Format_BGR888)
    pred_page.raw_img.setPixmap(QPixmap.fromImage(qImg))

def qimg2cv(qimg):
    buffer = qimg.bits()
    buffer.setsize(qimg.bytesPerLine()*qimg.height())
    if qimg.format().name == 'Format_BGR888':
        image = np.frombuffer(buffer, np.uint8).reshape((qimg.height(), qimg.width(), 3))
        # image = cv2.cvtColor(arr,cv2.COLOR_BGR2RGB)
    else:
        arr = np.frombuffer(buffer, np.uint8).reshape((qimg.height(), qimg.width(), 4))
        image = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)
    return image


# 图片位置到颜色的映射
def pos2color(pred_page,click_pos):
    x = click_pos.x()
    y = click_pos.y()
    x = min(max(0,x),img_width-1)
    y = min(max(0,y),img_height-1)
    raw_img = pred_page.clip_img_old        # 带框，后面就不需要再绘制框了
    current_img = qimg2cv(raw_img)
    color_set = current_img[y][x]
    return color_set

def pick_color(pred_page,color_set):
    raw_img = pred_page.clip_img_old        # 带框，后面就不需要再绘制框了
    current_img = qimg2cv(raw_img)
    # 更换按钮颜色
    color = '#' + str(hex(color_set[2]))[-2:].replace('x', '0').upper()
    color += str(hex(color_set[1]))[-2:].replace('x', '0').upper()
    color += str(hex(color_set[0]))[-2:].replace('x', '0').upper()
    pred_page.color_pre_btn.setStyleSheet(f'QPushButton {{background-color: {color};border: 1px solid blue}}')
    # 设置当前的颜色选择范围
    pred_page.mask_img = get_color_mask(color_set,current_img)
    # 更新图片
    refresh_img(pred_page,current_img)

def get_color_mask(color_set,current_img):
    if (color_set is not None):
        color = cv2.cvtColor(np.uint8([[color_set]]), cv2.COLOR_BGR2HSV)
        color_pixel = color[0][0]
        lower_color_lim = np.array([color_pixel[0] - 10, color_pixel[1] - 50, color_pixel[2] - 20])
        higher_color_lim = np.array([color_pixel[0] + 10, color_pixel[1] + 50, color_pixel[2] + 20])
        hsv = cv2.cvtColor(current_img,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv,lower_color_lim,higher_color_lim)
        return mask

def earse_color(pred_page,click_pos,earse_range = 10):
    x = click_pos.x()
    y = click_pos.y()
    x = min(max(0,x),img_width)
    y = min(max(0,y),img_height)
    y_range_up = max(y - earse_range,0)
    y_range_down = min(img_height,y + earse_range)
    x_range_left = max(x - earse_range,0)
    x_range_right = min(x + earse_range,img_width)
    # 更新mask_img
    if pred_page.mask_img is not None:
        pred_page.mask_img[y_range_up:y_range_down, x_range_left:x_range_right] = 0
    raw_img = pred_page.clip_img_old
    current_img = qimg2cv(raw_img)
    # 更新显示的图
    refresh_img(pred_page, current_img)

def check_area(pred_page):
    if pred_page.start_pos:
        area = abs(pred_page.end_pos.y() - pred_page.start_pos.y()) * abs(pred_page.end_pos.x() - pred_page.start_pos.x())
        if area < 10:
            QMessageBox.question(pred_page, '警告', "当前选中图形区域过小，请重新选择。", QMessageBox.StandardButton.Yes)
            pred_page.isTouched = False
            return False
    return True

# 预览
def color_extractor(pred_page):
    # 预览step1：画图的前提有mask
    if pred_page.mask_img is not None:
        if pred_page.start_pos is not None:
            tmp_mask = pred_page.mask_img[pred_page.start_pos.y():pred_page.end_pos.y(),pred_page.start_pos.x():pred_page.end_pos.x()]
        else:
            tmp_mask = pred_page.mask_img
        # 提取数据点
        extracted_data = extract_data(tmp_mask)
        # 数据点映射坐标
        mapped_data = data_mapping(pred_page,extracted_data,tmp_mask.shape[1],tmp_mask.shape[0])
        # 添加到dot_dict中
        legend = pred_page.stat_legend.text()
        pred_page.color_pre_btn.styleSheet()
        color = pred_page.color_pre_btn.palette().color(pred_page.color_pre_btn.backgroundRole()).name()
        pred_page.dot_dict[legend]=(color,mapped_data)
        show_stat(pred_page)
    else:
        QMessageBox.question(pred_page, '警告', "请先使用颜色选择工具提取图表颜色。", QMessageBox.StandardButton.Yes)

# 预览step2
def extract_data(tmp_mask):
    result = []
    # Here the width and height
    curve_range_height,curve_range_width = tmp_mask.shape
    for i in range(0,curve_range_width,1):
        # 如果有黑色像素，取中值
        # 注意行列和矩阵的维度的对应
        # 矩阵中，第一维为行，第二为列。所以对x坐标进行循环， 就应该取出对应的列的所有行
        if(255 in tmp_mask[:,i]):
            ldx = curve_range_height-np.median(np.argwhere(tmp_mask[:,i]==255))
            result.append([i,ldx])
    # log_print(array(result))
    return np.array(result)

# 预览step3
def data_mapping(pred_page,tmp_mask,width,height):
    data_spaced_x = tmp_mask[:,0]
    data_spaced_y = tmp_mask[:,1]
    x_min = float(pred_page.x_min_edit.text())
    x_max = float(pred_page.x_max_edit.text())
    y_min = float(pred_page.y_min_edit.text())
    y_max = float(pred_page.y_max_edit.text())
    data_spaced_x = data_spaced_x/width*(x_max-x_min)+x_min
    data_spaced_y = data_spaced_y/height*(y_max-y_min)+y_min
    return np.array([data_spaced_x,data_spaced_y]).T

def show_stat(pred_page):
    # 绘制前清空画布
    pred_page.figure.clf()
    ax = pred_page.figure.add_axes([0.1, 0.1, 0.8, 0.8])
    x_min = float(pred_page.x_min_edit.text())
    x_max = float(pred_page.x_max_edit.text())
    y_min = float(pred_page.y_min_edit.text())
    y_max = float(pred_page.y_max_edit.text())
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    for key,value in pred_page.dot_dict.items():
        if len(value[1][:,0])>0:
            ax.plot(value[1][:,0],value[1][:,1],label=key,color=value[0])
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('识别结果')
    pred_page.stat_graph.draw()
