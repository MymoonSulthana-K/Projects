import cv2, pandas
from datetime import datetime

# Load Haar Cascade for human detection
haarcascade_path = 'D:\Docs\Projects\Motion Activated Recording for Optimized Storage\haarcascade_fullbody.xml'
human_cascade = cv2.CascadeClassifier(haarcascade_path)

# Check if the cascade is loaded correctly
if human_cascade.empty():
    print("Error loading cascade classifier. Check the path to the XML file.")
    exit() 

# Assigning our static_back to None
static_back = None

# List when any moving object appear
motion_list = [None, None]

# Time of movement
movetime = []

# Initializing DataFrame, one column is start time and the other column is end time
df = pandas.DataFrame(columns=["Start", "End"])

# Capturing video
url="http://192.168.1.3:8080/video"
video = cv2.VideoCapture(url)#0 for webcam
fourcc = cv2.VideoWriter_fourcc(*'XVID')
name = str(datetime.now()).replace(':', "-")[:19]
path = 'D:\Docs\Projects\Motion Activated Recording for Optimized Storage\Detected at '+ name +'.avi'
out = cv2.VideoWriter(path, fourcc, 20.0, (640, 480))

# Load Haar Cascade for human detection
haarcascade_path = 'haarcascade_fullbody.xml'
human_cascade = cv2.CascadeClassifier(haarcascade_path)

# Infinite while loop to treat stack of images as video
while True:
    # Reading frame(image) from video
    check, frame = video.read()
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(frame, str(datetime.now()), (20, 40), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

    # Initializing motion = 0(no motion)
    motion = 0

    # Converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Converting gray scale image to GaussianBlur
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # In first iteration, assign the value of static_back to our first frame
    if static_back is None:
        static_back = gray
        continue

    # Difference between static background and current frame
    diff_frame = cv2.absdiff(static_back, gray)

    # Change this threshold value for sensitivity
    thresh_frame = cv2.threshold(diff_frame, 60, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Finding contours of moving objects
    cnts, _ = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 5000:  # Adjust contour area threshold
            continue
        motion = 1

        # Draw bounding box around detected motion
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Object detection to classify the detected area
        roi = gray[y:y + h, x:x + w]  # Region of interest
        humans = human_cascade.detectMultiScale(roi, scaleFactor=1.1, minNeighbors=5)

        if len(humans) == 0:  # If no humans detected in the ROI
            motion = 0  # Ignore the motion

    # Appending status of motion
    motion_list.append(motion)
    motion_list = motion_list[-2:]

    # Appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        movetime.append(datetime.now())

    if motion_list[0] == 1 and motion_list[1] == 1:
        out.write(frame)

    # Appending End time of motion
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        movetime.append(datetime.now())

    # Display frames
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Difference Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        if motion == 1:
            movetime.append(datetime.now())
        break

# Appending time of motion in DataFrame
for i in range(0, len(movetime), 2):
    df = df._append({"Start": movetime[i], "End": movetime[i + 1]}, ignore_index=True)

# Creating a CSV file in which time of movements will be saved
df.to_csv("Timestamps.csv")

video.release()
cv2.destroyAllWindows()
