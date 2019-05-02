import cv2

class VideoCamera:

    def __init__(self):
        self.video = cv2.VideoCapture(1)
        # self.video = cv2.VideoCapture('../test/vid/h264-night.mp4')
        self.video.set(cv2.cv2.CAP_PROP_FPS, 15)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read(cv2.IMREAD_GRAYSCALE)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, jpg = cv2.imencode('.jpg', gray)
        return jpg.tobytes()
