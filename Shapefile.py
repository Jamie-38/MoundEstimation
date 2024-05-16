from osgeo import ogr
from osgeo import osr
import os

class DetectionDataShapefile:
    def __init__(self, EPSG_code, directory=None, filename="Outfile.shp"):
        """
        Initialize the DetectionDataShapefile with the specified EPSG code, directory, and filename.
        
        Args:
            EPSG_code (int): The EPSG code for the spatial reference system.
            directory (str): The directory where the shapefile will be stored. Defaults to the current directory.
            filename (str): The name of the shapefile. Defaults to "Outfile.shp".
        """
        self.directory = directory
        self.filename = filename
        self.EPSG_code = EPSG_code
        self.data_source = None
        self.layer = None

    def open(self):
        """
        Open the shapefile for editing or create a new one if it does not exist.
        """
        full_path = os.path.join(self.directory, self.filename)
        driver = ogr.GetDriverByName("ESRI Shapefile")
        if os.path.exists(full_path):
            self.data_source = driver.Open(full_path, 1)  # Open existing file for editing
        else:
            self.data_source = driver.CreateDataSource(full_path)  # Create new file

        if self.data_source is None:
            raise ValueError("Could not open or create shapefile")

        self.setup_layer()

    def setup_layer(self):
        """
        Set up the layer in the shapefile. If the layer does not exist, create it with the appropriate spatial reference system and fields.
        """
        if self.data_source.GetLayerCount() == 0:
            srs = osr.SpatialReference()
            srs.ImportFromEPSG(int(self.EPSG_code))
            self.layer = self.data_source.CreateLayer("mound", srs, ogr.wkbPolygon)
            self.create_fields()
        else:
            self.layer = self.data_source.GetLayer()

    def create_fields(self):
        """
        Create fields for the layer to store detection data such as Confidence, Latitude, and Longitude.
        """
        field_confidence = ogr.FieldDefn("Confidence", ogr.OFTReal)
        self.layer.CreateField(field_confidence)
        field_lat = ogr.FieldDefn("Latitude", ogr.OFTReal)
        field_long = ogr.FieldDefn("Longitude", ogr.OFTReal)
        self.layer.CreateField(field_lat)
        self.layer.CreateField(field_long)

    def add_detections(self, detection):
        """
        Add a detection to the shapefile.
        
        Args:
            detection (object): The detection object containing confidence and geospatial coordinates.
        """
        # Create feature
        feature = ogr.Feature(self.layer.GetLayerDefn())
        
        # Set fields to detection object
        feature.SetField("Confidence", str(detection.confidence.item()))
        
        # Create geometry for feature
        geom = ogr.Geometry(ogr.wkbPolygon)
        ring = ogr.Geometry(ogr.wkbLinearRing)
    

        for coord in detection.geospatial_coords:
            ring.AddPoint(coord[0], coord[1])
        
        # Close the ring and add to polygon
        # Ensure the polygon is closed properly
        ring.CloseRings()  
        geom.AddGeometry(ring)
        
        feature.SetGeometry(geom)
        
        # Add feature to layer
        self.layer.CreateFeature(feature)
        
        # Destroy feature to free resources
        feature.Destroy()
        geom.Destroy()  # Ensure geometry is also destroyed


    def close(self):
        """
        Close the shapefile and release any resources.
        """
        if self.data_source:
            self.data_source = None




    
        