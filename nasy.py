import torch
from super_gradients.training import models
import cv2
import time
def get_video_capture(video, width=None, height=None, fps=None):
    """
     获得视频读取对象
     --   7W   Pix--> width=320,height=240
     --   30W  Pix--> width=640,height=480
     720P,100W Pix--> width=1280,height=720
     960P,130W Pix--> width=1280,height=1024
    1080P,200W Pix--> width=1920,height=1080
    :param video: video file or Camera ID
    :param width:   图像分辨率width
    :param height:  图像分辨率height
    :param fps:  设置视频播放帧率
    :return:
    """
    video_cap = cv2.VideoCapture(video)
    # 如果指定了宽度，高度，fps，则按照制定的值来设置，此处并没有指定
    if width:
        video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    if height:
        video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if fps:
        video_cap.set(cv2.CAP_PROP_FPS, fps)
    return video_cap

# 此处连接网络摄像头进行测试
#video_file = 'rtsp://账号:密码@ip/Streaming/Channels/1'
# video_file = 'data/output.mp4'
num_classes = 4
# best_pth = '/home/computer_vision/code/my_code/checkpoints/cars-from-above/ckpt_best.pth'
best_pth = '/Users/kachaicheung/PycharmProjects/YoloNas/ckc_best.pth'
device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
best_model = models.get("yolo_nas_s", num_classes=num_classes, checkpoint_path=best_pth).to(device)

'''开始计时'''
start_time = time.time()
video_cap = get_video_capture(0)
while True:
    isSuccess, frame = video_cap.read()
    if not isSuccess:
        break


    result_image = best_model.predict(frame, conf=0.45, fuse_model=False)
    #result_image = result_image._images_prediction_lst[0]
    result_image = result_image.draw()
    '''改动'''
    result_image = cv2.resize(result_image, (960, 540))
    '''end'''
    cv2.namedWindow('result', flags=cv2.WINDOW_NORMAL)
    cv2.imshow('result', result_image)
    kk = cv2.waitKey(1)
    if kk == ord('q'):
        break
video_cap.release()
'''时间结束'''
end_time = time.time()
run_time = end_time - start_time
print(run_time)
