from pykml import parser
from lxml import etree
import json
import os
from project_config import ProjectConfig

def extract_coordinates_from_kml():
    
    project_config = ProjectConfig()
        
    # Parse the KML file
    with open(project_config.points_kml_path) as f:
        root = parser.parse(f).getroot()

    # Extract coordinates from all the Placemark elements
    coordinates = []
    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        for point in placemark.findall('.//{http://www.opengis.net/kml/2.2}Point'):
            coords = point.coordinates.text.strip()
            longitude, latitude, altitude = coords.split(',')
            coordinates.append([float(latitude), float(longitude)])

    project_config.save_data_to_json(coordinates, project_config.points_json_path)

if __name__ == '__main__':
    extract_coordinates_from_kml()
