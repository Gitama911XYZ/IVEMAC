import cv2
from yolov5 import YOLOv5

# Initialize YOLOv5
yolo = YOLOv5("/Users/kachaicheung/PycharmProjects/yolov5ball/Ken120z120224.pt")

# Open the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")
# 假設你有一個類別名稱列表
class_names = ['basket','blueball','irrelevant','redball']


while True:
    # Read the current frame from the webcam
    ret, frame = cap.read()

    # Use YOLOv5 to detect objects in the frame
    results = yolo.predict(frame)

    # Filter results to only include detections with a confidence score > 0.5
    results_filtered = [detection for detection in results.xyxy[0] if detection[4] > 0.0]

    # Draw the filtered detection results on the frame
    for det in results_filtered:
        # det is a tensor with (x1, y1, x2, y2, confidence, class)
        x1, y1, x2, y2, conf, cls = int(det[0]), int(det[1]), int(det[2]), int(det[3]), det[4], int(det[5])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Draw rectangle
        cls = int(det[5])
        a = str(cls)
        class_name = class_names[cls]

        #cv2.putText(frame,cls, (x1, y1-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        cv2.putText(frame,class_name, (x1, y1 - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        cv2.putText(frame, f'{conf:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)  # Put confidence score

    # Display the frame
    cv2.imshow('YOLOv5 Webcam Object Detection', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
