from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class DetectionResult:
    """
    Dataclass to contain relevant feature data for detected mounds, including confidence score and geospatial coordinates.

    Attributes:
        confidence (float): The confidence score of the detection.
        geospatial_coords (List[Tuple[float, float]]): A list of tuples representing the geospatial coordinates (longitude, latitude) of the detected mound's mask.
    """
    confidence: float
    geospatial_coords: List[Tuple[float, float]] 
    

