# #!/usr/bin/env python3
#
# import cv2
# import depthai as dai
#
# # Create pipeline
# pipeline = dai.Pipeline()
#
# # Define source and output
# camRgb = pipeline.create(dai.node.ColorCamera)
# xoutRgb = pipeline.create(dai.node.XLinkOut)
#
# xoutRgb.setStreamName("rgb")
#
# # Properties
# camRgb.setPreviewSize(672, 384)
# #camRgb.setPreviewSize(300,300)
# # Rgb.setPreviewSize(608,812)
# # camRgb.setPreviewSize(1280,960)
# camRgb.setInterleaved(False)
# #camRgb.setMaxOutputFrameSize(1244160)
# camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)
#
# # Linking
# camRgb.preview.link(xoutRgb.input)
#
# # Connect to device and start pipeline
# with dai.Device(pipeline) as device:
#
#     print('Connected cameras:', device.getConnectedCameraFeatures())
#     # Print out usb speed
#     print('Usb speed:', device.getUsbSpeed().name)
#     # Bootloader version
#     if device.getBootloaderVersion() is not None:
#         print('Bootloader version:', device.getBootloaderVersion())
#     # Device name
#     print('Device name:', device.getDeviceName(), ' Product name:', device.getProductName())
#
#     # Output queue will be used to get the rgb frames from the output defined above
#     qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
#
#     while True:
#         inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
#
#         # Retrieve 'bgr' (opencv format) frame
#         cv2.imshow("rgb", inRgb.getCvFrame())
#
#         if cv2.waitKey(1) == ord('q'):
#             break
#
#

import cv2
import depthai as dai

# Create pipeline
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)

# Properties
camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_12_MP)


manip = pipeline.createImageManip()

# manip.setResizeThumbnail(1280, 720) # incompatible arguments : (self: depthai.node.ImageManip, arg0: int, arg1: int, arg2: int, arg3: int, arg4: int) -> None
# manip.initialConfig.setResizeThumbnail(1280, 720)  # Hangs

manip.initialConfig.setResizeThumbnail(1280, 720)  # Works but crops instead of padding
manip.setMaxOutputFrameSize(1280 * 720 * 3)
camRgb.isp.link(manip.inputImage)

out = pipeline.createXLinkOut()
out.setStreamName("manip")

manip.out.link(out.input)

# Connect to device and start pipeline
with dai.Device(pipeline) as device:

    manipq = device.getOutputQueue(name="manip")

    while True:
        cv2.imshow("manip", manipq.get().getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break