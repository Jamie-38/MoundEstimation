from Streamer import OrthoStreamer
from Model import MoundDetection
from Shapefile import DetectionDataShapefile
from Detection_Result import DetectionResult
from Interface_utils import mask_px_to_geospatial, calculate_total_size
import numpy as np

class DetectionInterface:
    def __init__(self, stream_path, model_path, shapefile_path):
        """
        Initailise the DetectionInterface along with the OrthoStreamer, MoundDetection and DetectionDataShapefile objects.
        Also set up a container for results and layout variables for memory management. 
        Detection results will be stored in a buffer that will be cleared once the allowance has been exceeded.
        
        Args: 
            stream_path (str): This is the path to the Orthophoto
            model_path (str): This is the path to the YOLOV8 model weights
            shapefile_path(str): This is the destination path for the shapefiles, these will contain the detection results
        """
        self.stream = OrthoStreamer(stream_path)
        self.detector = MoundDetection(model_path)
        self.shapefile = DetectionDataShapefile(self.stream.epsg_code, shapefile_path)
        self.detections = []
        self.total_memory_used = 0
        self.max_memory_allowance = 25 * 1024 * 1024  # 25 MB

    def process_sections(self):
        """
        Begin streaming and processing of the orthophoto.
        For each streamed section, check if the image has content and is not padding.
        If there is content, run detection, handle the results and manage memory.
        After all sections are streamed, finalise any remaining detections.         
        
        """
        for i, section in enumerate(self.stream.stream_sections()):
            # Check image has content, skip if not
            if np.all(section[0] == 0):
                print("No Content in Image")
                continue

            # Process image
            results = self.detector.predict_single_image(section[0])
            self.handle_detection_results(section, results)
            self.manage_memory()

        # After streaming all image, ensure any remaining results are taken care of.
        self.finalize_detections()

    def handle_detection_results(self, section, results):
        """
        Process the detection results for a given section of the orthophoto.
    
        The detection model returns a container of all detections in an image.
        For each detection result, if the result contains both masks and boxes, 
        the result can be processed using the section's geotransform.
    
        Args:
            section (tuple): A tuple containing the image section and its geotransform.
                section[0] is the image data (numpy array).
                section[1] is the geotransform tuple.
            results (list): A list of detection results from the model.
                Each result should contain masks and boxes attributes.
        """
        for result in results:
            if result.masks and result.boxes:
                self.process_result(section[1], result)

    def process_result(self, geotransform, result):
        """
        Process each detected mound by converting mask image coordinates to geospatial coordinates.
    
        Each detected mound will be contained in its own DetectionResult dataclass object.
        This is done by converting the mound's mask image coordinates to geospatial coordinates using the section geotransform.
        The DetectionResult dataclass will also contain the detection confidence.
        The dataclass object will then be stored in a buffer and its memory impact will be recorded for memory management.
    
        Args:
            geotransform (tuple): The geotransform tuple for the section, used to convert pixel coordinates to geospatial coordinates.
            result (object): The detection result object containing masks and boxes attributes.
        """
        for box, mask in zip(result.boxes, result.masks):
            geospatial_coords = mask_px_to_geospatial(geotransform, mask)
            detection = DetectionResult(box.conf, geospatial_coords)
            self.detections.append(detection)
            self.total_memory_used += calculate_total_size(detection)

    def manage_memory(self):
        """    
        This method checks if the total memory used by detection dataclass objects exceeds the maximum memory allowance.
        If it does, the current detections are dumped to a shapefile to free up memory.
        """
        if self.total_memory_used > self.max_memory_allowance:
            self.dump_to_shapefile()

    def dump_to_shapefile(self):
        """
        Uses the functionality of the DetectionDataShapefile class to either create or open an existing shapefile.
        Then proceeds to update the file with detection data before closing the file, clearing the detection data buffer and resetting the memory usage total.
        """
        self.shapefile.open()
        for detection in self.detections:
            self.shapefile.add_detections(detection)
        self.shapefile.close()
        self.detections.clear()
        self.total_memory_used = 0

    def finalize_detections(self):
        """
        If any data remains in the detection buffer ensure it is processed.
        """
        if self.detections:
            self.dump_to_shapefile()

if __name__ == "__main__":
    
    stream = 'E:\\projects\\mound_est\\ortho\\odm_orthophoto.tif'
    detector = 'C:\\Users\\Jayyy\\runs\\segment\\train\\weights\\best.pt'
    results_directory = 'E:\\projects\\mound_est\\shapefiles'
    
    interface = DetectionInterface(stream, detector, results_directory)
    interface.process_sections()
