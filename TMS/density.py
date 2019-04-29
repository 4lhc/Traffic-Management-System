import cv2
from urllib.request import urlopen
import numpy as np
import threading


class Density():
    def __init__(self, stream_url):
        """
        Start a thread which tracks traffic density
        """
        self.density = [0, 0, 0, 0]
        self.stream_url = stream_url
        self.template_files = ['test/img/template_roi_1.jpg',
                               'test/img/template_roi_2.jpg',
                               'test/img/template_roi_3.jpg',
                               'test/img/template_roi_4.jpg']
        self.templates = [cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)
                          for template_file in self.template_files]
        self.mask_files = ['test/img/mask_roi_1.jpg',
                           'test/img/mask_roi_2.jpg',
                           'test/img/mask_roi_3.jpg',
                           'test/img/mask_roi_4.jpg']
        self.masks = [cv2.imread(mask_file, cv2.IMREAD_GRAYSCALE)
                      for mask_file in self.mask_files]

        self.crop = [{"x1": 970, "y1": 400, "x2":1279, "y2":500},
                     {"x1": 755, "y1": 275, "x2":940, "y2":365},
                     {"x1": 335, "y1": 335, "x2":528, "y2":400},
                     {"x1": 300, "y1": 470, "x2":670, "y2":675}]

    def process_stream(self):
        """

        """
        with urlopen(self.stream_url) as stream:
            bytes = b''
            while True:
                bytes += stream.read(1024)
                a = bytes.find(b'\xff\xd8') #start bytes of mjpeg
                b = bytes.find(b'\xff\xd9') #end bytes of mjpeg
                if a != -1 and b != -1:     #detect start and end pos
                    jpg = bytes[a:b+2]      #extract jpeg
                    bytes = bytes[b+2:]     #next jpeg item
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR) #decode jpg raw bytes to np array
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    for index, (mask, template) in enumerate(zip(self.masks, self.templates)):
                        roi = cv2.bitwise_and(gray, gray, mask=mask)
                        x1 = self.crop[index]["x1"]
                        y1 = self.crop[index]["y1"]
                        x2 = self.crop[index]["x2"]
                        y2 = self.crop[index]["y2"]
                        roi = roi[y1:y2, x1:x2]
                        res = cv2.matchTemplate(roi, template, cv2.TM_CCORR_NORMED)
                        self.density[index] = res[0][0]

                    if cv2.waitKey(1) == 27: #wait for <ESC>
                        exit(0)

            cv2.destroyAllWindows()

    def begin_processing(self):
        """
        Start the thread
        """
        t = threading.Thread(target=self.process_stream)
        t.start()
