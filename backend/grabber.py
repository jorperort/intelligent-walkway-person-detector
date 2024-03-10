import cv2
import urllib.request
import pandas as pd
from ultralytics import YOLO
from tracker import Tracker
import cvzone
import numpy as np
from datetime import datetime

# Load the YOLO model
model = YOLO('yolov8s.pt')

# Function to handle mouse events in the 'RGB' window
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        point = [x, y]
        print(point)

# Configure the 'RGB' window and set the mouse callback function
cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# URL of the MJPEG video stream
url = "http://83.56.31.69/mjpg/video.mjpg"

# Open the video stream
stream = urllib.request.urlopen(url)

# Create a VideoCapture object to read frames from the stream
cap = cv2.VideoCapture()

# Set the VideoCapture object to use the MJPEG stream
cap.open(url)

# Read classes from coco.txt
my_file = open("classes.txt", "r")
data = my_file.read()
class_list = data.split("\n")

# Counters and structures for people tracking
count = 0
area = [(0, 494), (0, 170), (1019, 445), (1019, 494)]
tracker = Tracker()
persons = {}
last_processed_date = None

while True:
    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    if current_date != last_processed_date:
        # Reset the person count for the new day
        persons = {}

        # Update the current date
        last_processed_date = current_date

    # Read the next frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame
    frame = cv2.resize(frame, (1020, 500))

    # Make predictions with the YOLO model
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    detection_list = []

    # Filter detections to get only those of people
    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])

        c = class_list[d]
        if 'person' in c:
            detection_list.append([x1, y1, x2, y2])

    # Update the tracker with the new people detections
    bbox_id = tracker.update(detection_list)

    # Draw circles at the centers of detected people
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int(x3 + x4) // 2
        cy = int(y3 + y4) // 2

        # People inside the area
        result = cv2.pointPolygonTest(np.array(area, np.int32), ((cx, cy)), False)
        if result >= 0:
            cv2.circle(frame, (cx, cy), 4, (255, 0, 255), -1)
            cv2.rectangle(frame, (x3, y3), (x4, y4), (0, 0, 255), 2)
            cvzone.putTextRect(frame, f"{id}", (x3, y3), 1, 2)

            persons[id] = (cx, cy)

    # Draw the reference area on the frame
    cv2.polylines(frame, [np.array(area, np.int32)], True, (255, 0, 255), 2)

    # Show the frame in the 'RGB' window
    cv2.imshow("RGB", frame)

    # Write frame
    cv2.imwrite('database/processed_frame.jpg', frame)

    # Exit the loop when the Esc key is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

    df = pd.DataFrame({"Date": [current_date], "PersonCount": [len(persons)]})
    df.to_csv('database/data.csv', index=False, header=False)

print(f"\n\n{len(persons)}")

# Release resources
cap.release()
cv2.destroyAllWindows()
