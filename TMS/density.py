import cv2
from urllib.request import urlopen
import numpy as np
import threading
import json


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

        crop_file = "crop.json"
        with open(crop_file, 'r') as fp:
            self.crop = json.load(fp)

    def process_stream(self):
        """

        """
        with urlopen(self.stream_url) as stream:
            bytes = b''
            while True:
                bytes += stream.read(60*1024)
                a = bytes.find(b'\xff\xd8') #start bytes of mjpeg
                b = bytes.find(b'\xff\xd9') #end bytes of mjpeg
                if a != -1 and b != -1:     #detect start and end pos
                    jpg = bytes[a:b+2]      #extract jpeg
                    bytes = bytes[b+2:]     #next jpeg item
                    img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.COLOR_BGR2GRAY) #decode jpg raw bytes to np array
                    cv2.imshow("stream", img)
                    for index, (mask, template) in enumerate(zip(self.masks, self.templates)):
                        mask = np.uint8(mask)
                        img = np.uint8(img)
                        template = np.uint8(mask)
                        x1 = self.crop[index]["x1"]
                        y1 = self.crop[index]["y1"]
                        x2 = self.crop[index]["x2"]
                        y2 = self.crop[index]["y2"]
                        crop_img = img[y1:y2, x1:x2]
                        # print(index, crop_img.shape, mask.shape )
                        # print(crop_img.dtype, mask.dtype)
                        roi = cv2.bitwise_and(crop_img, crop_img, mask=mask)
                        # roi = roi[y1:y2, x1:x2]
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
        return t

    def get_max_density(self):
        """
        Return the position with max Density
        """
        return str(self.density.index(max(self.density)) + 1)
