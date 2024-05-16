import ultralytics
from ultralytics import YOLO


class MoundDetection:
    def __init__(self, pt_weights_path):
        """
        Initialize MoundDetection object with the YOLOv8 model.
        
        Perform necessary library checks, then load the model architecture and weights.
        
        Args:
            pt_weights_path (str): The path to the trained YOLOv8 weights.
        """
        ultralytics.checks()
        
        self.model_path = pt_weights_path
        self.model = YOLO(self.model_path)
        
    def predict_single_image(self, image):
        """
        Run detection on a single image and return results.
        
        Args:
            image (numpy.ndarray): The image on which to run detection.
            
        Returns:
            results: The detection results from the YOLO model.
        """
        results = self.model.predict(image)
        
        return results