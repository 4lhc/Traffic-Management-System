import cv2
import numpy as np

cap = cv2.VideoCapture(0)
pts = np.empty(shape=(0, 2), dtype=np.int32)
curr_coord = (0, 0)
window_name = "capture"
yellow = (0, 255, 255)
stroke = 2

def draw_polygon(frame, pts):
    if pts.shape[0] > 0 and pts.shape[0] <= 4:
        closed = (pts.shape[0] == 4) #True if size == 4
        cv2.polylines(frame, [pts.reshape((-1,1,2))], closed, yellow)
        if not closed:
            cv2.line(frame, tuple(pts[-1]), curr_coord, yellow, stroke)


def mouse_event(event, x, y, flag, param):
    global pts
    global curr_coord
    if event == cv2.EVENT_LBUTTONDOWN:
        pts = np.append(pts, [[x, y]], axis=0)
    if event == cv2.EVENT_MOUSEMOVE:
        curr_coord = (x, y)

cv2.namedWindow("capture")
cv2.setMouseCallback("capture", mouse_event)
while True:
    ret, frame = cap.read()
    draw_polygon(frame, pts)
    cv2.imshow("capture", frame)
    if pts.shape[0] > 4:
        fromCenter = False
        r = cv2.selectROI(frame, fromCenter)
        print(r)
        pts = np.empty(shape=(0, 2), dtype=np.int32)

    if cv2.waitKey(1) == 27:
        exit(0)

cap.release()
cv2.destroyAllWindows()
