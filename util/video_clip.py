# @Author      : Duhongkai
# @Time        : 2023/5/20 17:30
# @Description : 视频裁剪
import cv2
input_video_path = 'C:/Users/Never/Desktop/default_video.mp4'
output_video_path = 'C:/Users/Never/Desktop/default_video_clip.mp4'
start_time = 4 * 60
end_time = 5.5 * 60
cap = cv2.VideoCapture(input_video_path)
frame_rate = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

start_frame = int(start_time * frame_rate)
end_frame = int(end_time * frame_rate)
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

output_video = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (width, height))

for frame_idx in range(end_frame-start_frame+1):
    ret, frame = cap.read()

    if not ret:
        break

    # 进行裁剪操作，这里只是简单示例，你可以根据需要进行自定义的裁剪操作
    # cropped_frame = frame[:, :900, :]
    # 将裁剪后的帧写入输出视频对象
    output_video.write(frame)

cap.release()
output_video.release()