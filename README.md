# Traffic-Management-System
Control traffic lights based on the vehicle density at four regions of interest at a traffic intersection. Live video stream obtained from here.

---

#### Background Extraction

Calculate the weighted sum of the input image src and the accumulator dst so that dst becomes a running average of the frame sequence. [link](https://docs.opencv.org/2.4/modules/imgproc/doc/motion_analysis_and_object_tracking.html?highlight=accumulate#accumulateweighted)

<img src="https://docs.opencv.org/2.4/_images/math/7480f2f9ee402e9e85823d2644b8e1f8c263191a.png" alt="eqn" width="600"/>

---


Average Image


<img src="test/img/average.jpg" alt="Running verage" width="600"/>


---

#### Template Creation
with masks and average frame [cv2.bitwise_and()](https://docs.opencv.org/2.4.8/modules/core/doc/operations_on_arrays.html#bitwise-and)


Template 1|  Template 2|Template 3|Template 4
----|-------|---------|---------
![](test/img/template_roi_1.jpg) | ![](test/img/template_roi_2.jpg) | ![](test/img/template_roi_3.jpg) | ![](test/img/template_roi_4.jpg)


---

#### ROI Extraction

ROI 1|  ROI 2|ROI 3|ROI 4
----|-------|---------|---------
![](test/img/roi_1.jpg) | ![](test/img/roi_2.jpg) | ![](test/img/roi_3.jpg) | ![](test/img/roi_4.jpg)


---

#### Template Matching

ROI 1|  ROI 2|ROI 3|ROI 4
----|-------|---------|---------
![](test/img/roi_density_1.jpg) | ![](test/img/roi_density_2.jpg) | ![](test/img/roi_density_3.jpg) | ![](test/img/roi_density_4.jpg)

refer [TMS.ipynb](https://github.com/4lhc/Traffic-Management-System/blob/master/TMS.ipynb) for more.
