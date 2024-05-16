import sys

def mask_px_to_geospatial(section_geotransform, mask):
    """
    Converts pixel coordinates in a mask to geospatial coordinates using the provided geotransform.
    
    Args:
        section_geotransform (tuple): A tuple representing the geotransform of the image section.
            It typically contains six coefficients:
                - top left x (longitude)
                - w-e pixel resolution
                - row rotation (typically zero)
                - top left y (latitude)
                - column rotation (typically zero)
                - n-s pixel resolution (negative value)
        mask (object): The mask object containing pixel coordinates (x, y).
            The object should have an attribute `xy` which provides the pixel coordinates.
    
    Returns:
        list of tuple: A list of (longitude, latitude) tuples representing the geospatial coordinates.
    """
    
    geospatial_coords = []
    # Iterate over the mask coordinate arrays
    for coordinate_array in mask.xy:
        # Iterate over coordinate pairs in mask
        for (px, py) in coordinate_array:
            # Apply the geotransform to convert pizerl coordinates to geospatial coordinates
            lon = section_geotransform[0] + px * section_geotransform[1] + py * section_geotransform[2]
            lat = section_geotransform[3] + px * section_geotransform[4] + py * section_geotransform[5]
            geospatial_coords.append((lon, lat))

    return geospatial_coords


def calculate_total_size(obj, seen=None):
    """
    Recursively calculates the total memory size of an object in bytes.
    
    Args:
        obj (object): The object whose size is to be calculated.
        seen (set, optional): A set of object IDs that have already been processed to avoid double-counting.
    
    Returns:
        int: Total memory size of the object in bytes.
    """
    if seen is None:
        seen = set()
    
    # Add object's id to seen to avoid processing the same object multiple times
    object_id = id(obj)
    if object_id in seen:
        return 0
    seen.add(object_id)
    
    size = sys.getsizeof(obj)
    
    if isinstance(obj, dict):
        size += sum((calculate_total_size(k, seen) + calculate_total_size(v, seen)) for k, v in obj.items())
    elif hasattr(obj, '__dict__'):
        size += calculate_total_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum(calculate_total_size(i, seen) for i in obj)
    
    return size
