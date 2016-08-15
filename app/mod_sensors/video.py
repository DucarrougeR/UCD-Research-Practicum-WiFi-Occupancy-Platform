import cv2, sys, os, time, numpy

def monitor(room):
    """
    Looks for faces in 30-second intervals using Haar cascade classifiers and outputs
    the results to a .csv file. 
    """

    # Calls Bash to generate the CSV file and print headings. 
    filename = os.popen('dir="data/"; now=$(date "+%d-%m-%Y-%H:%M:%S"); format=".csv"; filename=$dir$1$now$format; echo $filename').read().strip()
    cmd = 'printf "room,date,month,year,time,face" >> "{0}"'.format(filename)
    os.system(cmd)

    while True: 
        # For 30 seconds:
        loop_time = time.time() + 30
        while time.time() < loop_time:
            # Specifies and instantiates the classifier used.
            cascPath = "haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(cascPath)
            
            # Captures a video frame by frame. 
            video_capture = cv2.VideoCapture(0)
            ret, frame = video_capture.read()

            # Converts the image to greyscale.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detects faces using the classifier. 
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=10,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Sleeps for 2 seconds so there aren't too many frames to process. 
            time.sleep(2)

        # Writes to the outfile whether a face was detected or not. 
        if numpy.any(faces):
            os.system('printf "\n{0},$(date "+%d,%m,%Y,%H:%M:%S"),1", >> "{1}"'.format(room, filename))
        else:
            os.system('printf "\n{0},$(date "+%d,%m,%Y,%H:%M:%S"),0", >> "{1}"'.format(room, filename))
            
        # Releases the capture. 
        video_capture.release()
        cv2.destroyAllWindows()

monitor("B002")
