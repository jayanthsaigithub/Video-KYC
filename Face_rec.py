#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2

# Load pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect and highlight faces in an image
def detect_faces(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Draw a red rectangle around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)
    
    return image

# Function to capture image from camera
def capture_image():
    # Open the default camera
    cap = cv2.VideoCapture(0)
    
    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the camera")
        return None
    
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Release the camera
    cap.release()
    
    if ret:
        return frame
    else:
        print("Error: Unable to capture frame from the camera")
        return None

# Main function
def main():
    # Capture an image from the camera
    print("Capturing image from the camera...")
    image = capture_image()
    
    if image is not None:
        # Detect and highlight faces in the captured image
        print("Detecting faces...")
        image_with_faces = detect_faces(image)
        
        # Display the image with highlighted faces
        cv2.imshow('Face Detection', image_with_faces)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()


# In[ ]:




