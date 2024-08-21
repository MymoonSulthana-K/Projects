# Webcam Motion Detector
import cv2, pandas
from datetime import datetime

# Assigning our static_back to None
static_back = None

# List when any moving object appear
motion_list = [ None, None ]

# Time of movement
movetime = []

# Initializing DataFrame, one column is start
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])

# Capturing video
url="http://192.168.1.2:8080/video"
video = cv2.VideoCapture(url)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
name=str(datetime.now())
name=name[11:19].replace(':',"-")
path='Detected at '+ name +'.avi'
out = cv2.VideoWriter(path,fourcc, 20.0, (640,480))

# Infinite while loop to treat stack of image as video
while True:
	# Reading frame(image) from video
	check, frame = video.read()
	font = cv2.FONT_HERSHEY_PLAIN
	cv2.putText(frame, str(datetime.now()), (20, 40),font, 2, (255, 255, 255), 2, cv2.LINE_AA)

	# Initializing motion = 0(no motion)
	motion = 0

	# Converting color image to gray_scale image
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Converting gray scale image to GaussianBlur
	# so that change can be find easily
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# In first iteration we assign the value
	# of static_back to our first frame
	if static_back is None:
		static_back = gray
		continue

	# Difference between static background
	# and current frame(which is GaussianBlur)
	diff_frame = cv2.absdiff(static_back, gray)

	# If change in between static background and
	# current frame is greater than 30 it will show white color(255)
	thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
	thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

	# Finding contour of moving object
	cnts,_ = cv2.findContours(thresh_frame.copy(),
					cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for contour in cnts:
		if cv2.contourArea(contour) < 10000:
			continue
		motion = 1
	
		(x, y, w, h) = cv2.boundingRect(contour)
		# making green rectangle around the moving object
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

	
	# Appending status of motion
	motion_list.append(motion)
	
	motion_list = motion_list[-2:]
	#print(motion_list)
	
	# Appending Start time of motion
	if motion_list[-1] == 1 and motion_list[-2] == 0:
		movetime.append(datetime.now())
		
	if motion_list[0]==1 and motion_list[1]==1:
		out.write(frame)
	
	# Appending End time of motion
	if motion_list[-1] == 0 and motion_list[-2] == 1:
		movetime.append(datetime.now())

	# Displaying image in gray_scale
	cv2.imshow("Gray Frame", gray)

	# Displaying the difference in currentframe to
	# the staticframe(very first_frame)
	cv2.imshow("Difference Frame", diff_frame)

	# Displaying the black and white image in which if
	# intensity difference greater than 30 it will appear white
	cv2.imshow("Threshold Frame", thresh_frame)

	# Displaying color frame with contour of motion of object
	cv2.imshow("Color Frame", frame)

	key = cv2.waitKey(1)
	# if q entered whole process will stop
	if key == ord('q'):
		# if something is movingthen it append the end time of movement
		if motion == 1:
			movetime.append(datetime.now())
		break


# Appending time of motion in DataFrame
for i in range(0, len(movetime), 2):
	df = df._append({"Start":movetime[i], "End":movetime[i + 1]}, ignore_index = True)

# Creating a CSV file in which time of movements will be saved
df.to_csv("Timestamps.csv")

video.release()
# Destroying all the windows
cv2.destroyAllWindows()
