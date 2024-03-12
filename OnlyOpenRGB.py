#!/usr/bin/env python3

import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Define source and outputs
camRgb = pipeline.create(dai.node.ColorCamera)
xoutVideo = pipeline.create(dai.node.XLinkOut)


xoutVideo.setStreamName("video")

# Properties

camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
camRgb.setInterleaved(True)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

# Linking
camRgb.video.link(xoutVideo.input)


# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    video = device.getOutputQueue('video')


    while True:
        videoFrame = video.get()


        # Get BGR frame from NV12 encoded video frame to show with opencv
        cv2.imshow("video", videoFrame.getCvFrame())


        if cv2.waitKey(1) == ord('q'):
            break

