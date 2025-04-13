import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow as tf
#from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

# Load trained accident detection model
model = keras.models.load_model("mymodel.h5",compile = False) 

def preprocess_frame(frame):
    frame = cv2.resize(frame, (256, 256))  #(None, 256, 256, 3)
    frame = frame / 255.0  # Normalize
    return np.expand_dims(frame, axis=0)

def send_email_alert():
    sender_email = "sendermail@gmail.com"
    receiver_email = "examplemail2@gmail.com"
    password = "prodhifh'lakj"
    
    subject = "🚨 Accident Alert!"
    body = "An accident has been detected. Please respond immediately."
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
    
    print("Email Alert Sent!")

def detect_accident(video_file):
    cap = cv2.VideoCapture(video_file)
    stframe = st.empty()
    
    alert_sent = False  # Flag to track if an alert has been sent

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        processed_frame = preprocess_frame(frame)
        prediction = model.predict(processed_frame)
        
        if prediction[0][0] > 0.5 and not alert_sent:
            st.error("🚨 Accident Detected! Sending Alert...")
            send_email_alert()
            alert_sent = True  # Set flag to True so only one email is sent
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")
    
    cap.release()

def main():
    st.title("🚦 Real-Time Accident Detection")
    st.sidebar.title("Upload or Stream CCTV Footage")
    
    video_file = st.sidebar.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    
    if video_file is not None:
        st.sidebar.success("Processing video...")
        detect_accident(video_file.name)
    
    st.sidebar.write("Or use a live camera feed (Future feature)")

if __name__ == "__main__":
    main()

#pip install streamlit tensorflow opencv-python twilio
#streamlit run app.py