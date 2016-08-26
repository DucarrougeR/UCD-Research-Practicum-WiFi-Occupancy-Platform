import cv2, sys, os, time, numpy

def monitor(room):
    """
    Looks for faces in 30-second intervals using Haar cascade classifiers and outputs
    the results to a .csv file. 
    """

    # Calls Bash to generate the CSV file and print headings. 
    filename = os.popen('dir="data/"; now=$(date "+%d-%m-%Y-%H-%M-%S"); format=".csv"; filename=$dir$1$now$format; echo $filename').read().strip()
    cmd = 'printf "room,date,month,year,time,face" >> "{0}"'.format(filename)
    os.system(cmd)

    # Specifies and instantiates the classifier used.
    cascpath = "haarcascade_frontalface_default.xml"
    facecascade = cv2.CascadeClassifier(cascpath)

    while True: 
        face_detected = False

        # For 30 seconds:
        loop_time = time.time() + 30
        while time.time() < loop_time:
            # Captures a video frame by frame. 
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()

            # Converts the image to greyscale.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detects faces using the classifier. 
            faces = facecascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=10, 
                    minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('Video', frame)
            

            # Records if any faces were detected. 
            if numpy.any(faces):
                face_detected = True

            # Sleeps for 2 seconds so there aren't too many frames to process. 
            time.sleep(2)            

        # Writes to the outfile whether a face was detected or not. 
        if face_detected:
            os.system('printf "\n{0},$(date "+%d,%m,%Y,%H:%M:%S"),1", >> "{1}"'.format(room, filename))
        else:
            os.system('printf "\n{0},$(date "+%d,%m,%Y,%H:%M:%S"),0", >> "{1}"'.format(room, filename))

        # Releases the capture. 
        video_capture.release()

monitor("B002")
