from osgeo import gdal
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import re
    

class OrthoStreamer:
    def __init__(self, orthophoto_path):
        """
        Initialise the OrthoStreamer with the path to the orthophoto.
        """
        self.ortho_path = orthophoto_path
        self.dataset = gdal.Open(orthophoto_path, gdal.GA_ReadOnly)

        if self.dataset is None:
            raise ValueError(f"Failed to open the orthophoto: {orthophoto_path}")
            
        else:
            print("File opened successfully.")
            print("Raster dataset dimensions: {width}x{height}".format(width=self.dataset.RasterXSize, height=self.dataset.RasterYSize))
            print("Number of bands: {}".format(self.dataset.RasterCount))            
            self.epsg_code = self.get_epsg_code()
            print("EPSG Code: " + self.epsg_code)

                   
        
    
    def get_epsg_code(self):
        """
        Extract the EPSG code from the dataset's projection.
        """
        projection = self.dataset.GetProjection()
        # Find all EPSG codes in the projection string
        matches = re.findall(r'AUTHORITY\["EPSG","(\d+)"\]', projection)
        if matches:
            # Return the last EPSG code found
            return matches[-1]
        else:
            print("Unable to Get EPSG code from Image")
            return None

    def stream_sections(self, section_size=(512, 512)):
        """
        Generator to stream sections of the orthophoto.
        
        Args:
            section_size (tuple): The size of the sections to stream (width, height).
        
        Yields:
            section (ndarray): The image section.
            new_geotransform (tuple): The geotransform of the section.
        """
        
        # Get Orthophoto dimensions and Geotransform
        width, height = self.dataset.RasterXSize, self.dataset.RasterYSize
        geotransform = self.dataset.GetGeoTransform()
        
        # Iterate through Orthophoto in steps of Section_size
        for x in range(0, width, section_size[0]):
            for y in range(0, height, section_size[1]):
                
                # Determine the width and height of the current section 
                # Ensure the section does exceed Orthophoto boundary
                sec_width = min(section_size[0], width - x)
                sec_height = min(section_size[1], height - y)
    
                section = self.dataset.ReadAsArray(x, y, sec_width, sec_height)
                if section is not None:
                    # Adjust the geotransform for the current section
                    # The new origin of the section is (x, y) in pixel coordinates,
                    # which needs to be converted to geospatial coordinates
                    new_origin_x = geotransform[0] + x * geotransform[1] + y * geotransform[2]
                    new_origin_y = geotransform[3] + x * geotransform[4] + y * geotransform[5]
                    new_geotransform = (new_origin_x, geotransform[1], geotransform[2],
                                        new_origin_y, geotransform[4], geotransform[5])
                    
                    # Transpose the section to match format height, width, bands
                    section = section.transpose((1, 2, 0))
                    section  = section[ :, :, :3]
                    # Ensure section is contiguos for processing
                    section = np.ascontiguousarray(section)

                    yield section, new_geotransform


                
    def display_section(self, section):
        """
        Display a section of the orthophoto.
        
        Args:
            section (tuple): The image section and its geotransform.
        """
        if section is not None:
            plt.imshow(section[0])
            plt.show()
            print(section[1])
        else:
            print("Section is None.")
            
    def save_section_as_png(self, section, output_path):
        """
        Save a section of the orthophoto as a PNG file.
        
        Args:
            section (ndarray): The image section to save.
            output_path (str): The path to save the PNG file.
        """
        if section is not None:
            # If the section has more than 3 bands, select only the first three (RGB)
            if section.shape[0] > 3:
                section = section[:, :, :3]
    
            # Assuming the section is now RGB, convert the numpy array to an Image object
            image = Image.fromarray(section.astype("uint8"), "RGB")
    
            image.save(output_path)
        else:
            print("Section is None.")
                
