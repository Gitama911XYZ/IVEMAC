# # import the opencv library
# import cv2
# import math
# import runpy as np
# # define a video capture object
# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
# x =640 // 2
# y =490 // 2
#
#
#
# def cicle(frame):
#     center_coordinates = (x,y)
#     radius = 20
#     cv2.circle(frame, center_coordinates, radius, (255, 0, 0), 2)
# while (True):
#
#     # Capture the video frame
#     # by frame
#     ret, frame = vid.read()
#     cicle(frame)
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
#
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # After the loop release the cap object
# vid.release()
# # Destroy all the windows
# cv2.destroyAllWindows()

# import cv2
#
# # Define a video capture object
# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
#
# x = 640 // 2
# y = 490 // 2
#
# def circle(frame):
#     global x, y
#     center_coordinates = (x, y)
#     radius = 20
#     cv2.circle(frame, center_coordinates, radius, (255, 0, 0), 2)
#     return center_coordinates, radius
#
# while True:
#     # Capture the video frame
#     ret, frame = vid.read()
#
#     # Draw the circle on the frame and get circle details
#     center_coordinates, radius = circle(frame)
#
#     # Extract the region of interest (ROI) within the circle
#     roi = frame[center_coordinates[1] - radius:center_coordinates[1] + radius,
#                  center_coordinates[0] - radius:center_coordinates[0] + radius]
#
#     # Convert the ROI to HSV color space
#     hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#
#     # Compute the average HSV values within the ROI
#     average_hsv = cv2.mean(hsv_roi)
#
#     # Display the resulting frame
#     cv2.imshow('frame', frame)
#
#     # Print the average HSV values
#     print("Average HSV:", average_hsv)
#
#     # Check for the 'q' key to quit
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# # Release the video capture object and destroy the windows
# vid.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np

# Define a video capture object
vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)


# Default HSV values for the upper and lower bounds
lower_hsv = np.array([0, 0, 0])
upper_hsv = np.array([255, 255, 255])

x = 1920 // 2
y = 520
radius = 40

def on_trackbar_lower_hue(value):
    global lower_hsv
    lower_hsv[0] = value

def on_trackbar_upper_hue(value):
    global upper_hsv
    upper_hsv[0] = value

def on_trackbar_lower_saturation(value):
    global lower_hsv
    lower_hsv[1] = value

def on_trackbar_upper_saturation(value):
    global upper_hsv
    upper_hsv[1] = value

def on_trackbar_lower_value(value):
    global lower_hsv
    lower_hsv[2] = value

def on_trackbar_upper_value(value):
    global upper_hsv
    upper_hsv[2] = value

def circle(frame):
    global x, y, radius
    center_coordinates = (x, y)
    cv2.circle(frame, center_coordinates, radius, (255, 0, 0), 2)

while True:
    # Capture the video frame
    ret, frame = vid.read()

    # Draw the circle on the frame
    circle(frame)

    # Create a named window for trackbars
    cv2.namedWindow("Trackbars")

    # Create trackbars for lower and upper HSV values
    cv2.createTrackbar("Lower H", "Trackbars", lower_hsv[0], 255, on_trackbar_lower_hue)
    cv2.createTrackbar("Upper H", "Trackbars", upper_hsv[0], 255, on_trackbar_upper_hue)
    cv2.createTrackbar("Lower S", "Trackbars", lower_hsv[1], 255, on_trackbar_lower_saturation)
    cv2.createTrackbar("Upper S", "Trackbars", upper_hsv[1], 255, on_trackbar_upper_saturation)
    cv2.createTrackbar("Lower V", "Trackbars", lower_hsv[2], 255, on_trackbar_lower_value)
    cv2.createTrackbar("Upper V", "Trackbars", upper_hsv[2], 255, on_trackbar_upper_value)

    # Extract the region of interest (ROI) within the circle
    roi = frame[y - radius:y + radius, x - radius:x + radius]

    # Convert the ROI to HSV color space
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Create a mask based on the lower and upper HSV values
    mask = cv2.inRange(hsv_roi, lower_hsv, upper_hsv)

    # Apply the mask to the ROI
    masked_roi = cv2.bitwise_and(roi, roi, mask=mask)

    # Display the resulting frame and masked ROI
    cv2.imshow('frame', frame)
    cv2.imshow('masked ROI', masked_roi)

    # Check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and destroy the windows
vid.release()
cv2.destroyAllWindows()