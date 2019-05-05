import cv2

class VideoCamera:

    def __init__(self):
        self.video = cv2.VideoCapture(0) #set capture device
        # self.video = cv2.VideoCapture('../test/vid/h264-1.mp4')
        self.video.set(cv2.cv2.CAP_PROP_FPS, 15) #set framerate in fps

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grayscale
        ret, jpg = cv2.imencode('.jpg', gray) #encode numpy array to jpeg
        return jpg.tobytes()                  #send jpg as bytes
