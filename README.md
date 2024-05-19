This is the core functionality of my Master's dissertation project updated from Mask-rcnn to YOLOV8.

The project's task intended to take aerial images captured by drone during the mounding stage of site preparation and determine mounding density.

The project did this by first taking the drone images and creating an orthophoto of the site.
This was done using WebODM - Fast Ortho

An orthophoto provides a way to produce a georeferenced image, this was necessary as the original image data only contained drone GPS data at the location the image was captured.
As such each mound can be given accurate location data and not estimated. In the absence of ground control points or other methods, this was found to be the most robust solution. 

This orthophoto is then split into smaller sections for processing with a model, this is done to, reduce the resource cost of running the detection model and reduce the labelling effort.
Splitting is done in such a way as to preserve the feature resolution and not lose any information.

The detection results can then be combined with geotransform data to produce accurate mound location data. Both the original mask-rcnn project and YOLOV8 projects store mound data in shapefiles for simplicity.

To visualise the results, the project used QGIS

Both the Mask-rcnn and YOLOv8 models used COCO weights as a basis for training. however, as this YOLOV8 version is a prototype, training was done using default parameters.
The Yolov8 model was trained in two phases, the first phase used a manually labelled dataset of around 200 images(with augmentation) and was trained for 100 epochs.
This model was then used to annotate the rest of the dataset, producing over 3400 images with augmentations.
This additional data, following review, was then used to further train for another 100 epochs.

Further training will likely lead to better results but this is not practical as the project currently has no access to a GPU.

The mask-rcnn implementation followed a similar training approach but required additional functionalities in the code that YOLOV8 did not.
The original project needed a secondary focus on building utilities to support generating additional training data. 
This has not been needed with YOLOv8 because of its approach to training data.
In addition, the original mask-rcnn implementation also had the ability to evaluate its model. Functionality that is not added here.

Below is an example of the project results, the processed orthophoto of a site and a close-up view of detected mounds.

![siet_image](https://github.com/Jamie-38/MoundEstimation/assets/85198881/344196bd-e15e-4981-8838-592a609e5744)




![zoom](https://github.com/Jamie-38/MoundEstimation/assets/85198881/d7c9fd15-91b1-4caa-8c96-8d1c5f3aa8ce)
