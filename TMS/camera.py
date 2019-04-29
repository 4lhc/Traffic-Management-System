import cv2

class VideoCamera:

    def __init__(self):
        # self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture('../test/vid/h264-night.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()
