#!/usr/bin/env python3

import cv2
import numpy as np
import depthai as dai
import argparse




fps = 30
# The disparity is computed at this resolution, then upscaled to RGB resolution
monoResolution = dai.MonoCameraProperties.SensorResolution.THE_720_P

# Create pipeline
pipeline = dai.Pipeline()
device = dai.Device()
# queueNames = []

# Define sources and outputs
camRgb = pipeline.create(dai.node.Camera)
left = pipeline.create(dai.node.MonoCamera)
right = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)

rgbOut = pipeline.create(dai.node.XLinkOut)
disparityOut = pipeline.create(dai.node.XLinkOut)

rgbOut.setStreamName("rgb")
# queueNames.append("rgb")
disparityOut.setStreamName("disp")


#Properties
rgbCamSocket = dai.CameraBoardSocket.CAM_A

camRgb.setBoardSocket(rgbCamSocket)
camRgb.setSize(1920, 1080)
camRgb.setFps(fps)

# For now, RGB needs fixed focus to properly align with depth.
# This value was used during calibration
# try:
#     calibData = device.readCalibration2()
#     lensPosition = calibData.getLensPosition(rgbCamSocket)
#     if lensPosition:
#         camRgb.initialControl.setManualFocus(lensPosition)
# except:
#     raise
left.setResolution(monoResolution)
left.setCamera("left")
left.setFps(fps)
right.setResolution(monoResolution)
right.setCamera("right")
right.setFps(fps)
print(monoResolution)
stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# LR-check is required for depth alignment
stereo.setLeftRightCheck(True)
stereo.setDepthAlign(rgbCamSocket)

# Linking
camRgb.video.link(rgbOut.input)
left.out.link(stereo.left)
right.out.link(stereo.right)
stereo.disparity.link(disparityOut.input)

camRgb.setMeshSource(dai.CameraProperties.WarpMeshSource.CALIBRATION)


# Connect to device and start pipeline
with device:
    device.startPipeline(pipeline)

    frameRgb = None
    frameDisp = None

    # Configure windows; trackbar adjusts blending ratio of rgb/depth
    rgbWindowName = "rgb"
    depthWindowName = "depth"
    blendedWindowName = "rgb-depth"
    cv2.namedWindow(rgbWindowName)
    cv2.namedWindow(depthWindowName)
    cv2.namedWindow(blendedWindowName)


    while True:
        latestPacket = {}
        latestPacket["rgb"] = None
        latestPacket["disp"] = None

        queueEvents = device.getQueueEvents(("rgb", "disp"))
        for queueName in queueEvents:
            packets = device.getOutputQueue(queueName).tryGetAll()
            if len(packets) > 0:
                latestPacket[queueName] = packets[-1]

        if latestPacket["rgb"] is not None:
            frameRgb = latestPacket["rgb"].getCvFrame()
            cv2.imshow(rgbWindowName, frameRgb)

        if latestPacket["disp"] is not None:
            frameDisp = latestPacket["disp"].getFrame()
            maxDisparity = stereo.initialConfig.getMaxDisparity()
            # Optional, extend range 0..95 -> 0..255, for a better visualisation
            if 1: frameDisp = (frameDisp * 255. / maxDisparity).astype(np.uint8)
            # Optional, apply false colorization
            if 1: frameDisp = cv2.applyColorMap(frameDisp, cv2.COLORMAP_HOT)
            frameDisp = np.ascontiguousarray(frameDisp)
            cv2.imshow(depthWindowName, frameDisp)



        if cv2.waitKey(1) == ord('q'):
            break