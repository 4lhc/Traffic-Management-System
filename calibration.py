import cv2
import numpy as np
import time
from urllib.request import urlopen
import json

intersection_count = 4

stream_url = "http://0.0.0.0:5000/video_feed"
pts = np.empty(shape=(0, 2), dtype=np.int32)
crop = []
crop_file = "crop.json"
curr_coord = (0, 0)
window_name = "capture"
yellow = (0, 255, 255)
stroke = 2

template_file = 'test/img/template_roi_{}.jpg'
mask_file = 'test/img/mask_roi_{}.jpg'


def draw_polygon(frame, pts):
    if pts.shape[0] > 0 and pts.shape[0] <= 4:
        closed = (pts.shape[0] == 4) #True if size == 4
        cv2.polylines(frame, [pts.reshape((-1,1,2))], closed, yellow)
        if not closed:
            cv2.line(frame, tuple(pts[-1]), curr_coord, yellow, stroke)

def crop_frame(img, pts):
    xs = pts[:,0]
    ys = pts[:,1]
    #finding bounding box
    x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
    #cropped img returned
    d = {"x1":int(x1), "x2":int(x2), "y1":int(y1), "y2":int(y2) }

    if d not in crop:
        crop.append(d)
    return img[y1:y2, x1:x2]


def mouse_event(event, x, y, flag, param):
    global pts
    global curr_coord
    if event == cv2.EVENT_LBUTTONDOWN:
        pts = np.append(pts, [[x, y]], axis=0)
    if event == cv2.EVENT_MOUSEMOVE:
        curr_coord = (x, y)

for i in range(intersection_count):
    pts = np.empty(shape=(0, 2), dtype=np.int32)
    cv2.namedWindow("capture")
    cv2.setMouseCallback("capture", mouse_event)
    with urlopen(stream_url) as stream:
        bytes = b''

        while True:
            bytes += stream.read(60*1024)
            a = bytes.find(b'\xff\xd8') #start bytes of mjpeg
            b = bytes.find(b'\xff\xd9') #end bytes of mjpeg
            if a != -1 and b != -1:     #detect start and end pos
                jpg = bytes[a:b+2]      #extract jpeg
                bytes = bytes[b+2:]     #next jpeg item
                gray = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.COLOR_BGR2GRAY) #decode jpg raw bytes to np array
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # gray = np.uint8(gray)
                mask = np.zeros(gray.shape, dtype=np.uint8)
                # mask.fill(0)
                draw_polygon(gray, pts)
                cv2.imshow("capture", gray)
                if pts.shape[0] >= 4:
                    mask = cv2.fillPoly(mask, [pts] , 255)
                    #cropping
                    mask = crop_frame(mask, pts)
                    gray = crop_frame(gray, pts)
                    roi = cv2.bitwise_and(gray, gray, mask=mask)
                    cv2.imwrite(mask_file.format(i+1), mask)
                    cv2.imwrite(template_file.format(i+1),roi)
                    break

            if cv2.waitKey(1) == 27:
                exit(0)

cv2.destroyAllWindows()

with open(crop_file, 'w') as fp:
    json.dump(crop, fp)
