import numpy as np
from pykml.factory import KML_ElementMaker as KML
from lxml import etree
from project_config import ProjectConfig

def convert_to_kml():
    project_config = ProjectConfig()

    points, groups, plant_nums = project_config.get_map_data()

    # Create a KML document
    doc = KML.kml(
        KML.Document(
            KML.name("Bush Locations"),
        )
    )

    # Define a style with a small red dot icon
    red_dot_style = KML.Style(
        KML.IconStyle(
            KML.Icon(
                KML.href("http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png")
            ),
            KML.color("ff0000ff"),
            KML.scale(0.5)  # Adjust the scale as needed
        ),
        id="red_dot_style"
    )
    doc.Document.append(red_dot_style)

    # Define a style with a small white dot icon
    white_dot_style = KML.Style(
        KML.IconStyle(
            KML.Icon(
                KML.href("http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png")
            ),
            KML.color("ffffffff"),
            KML.scale(0.5)  # Adjust the scale as needed
        ),
        id="white_dot_style"
    )
    doc.Document.append(white_dot_style)

    # Add placemarks to the document
    for i in range(len(points)):
        lat, lon = points[i]
        group_number = groups[i]
        bush_number = plant_nums[i]
        group_type = project_config.get_group_name(group_number)
        
        if group_type == 'Post':
            style_url = "#white_dot_style"
            description_str = f"Group number: {group_number} \n Group type: {group_type}"
        else:
            style_url = "#red_dot_style"
            description_str = f"Bush number: {bush_number} \n Group number: {group_number} \n Group type: {group_type}"
        placemark = KML.Placemark(
            KML.styleUrl(style_url),
            KML.description(description_str),
            KML.Point(
                KML.coordinates(f"{lon},{lat}")
            )
        )
        doc.Document.append(placemark)

    # Convert to string and write to a file
    kml_str = etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    with open(project_config.map_data_kml_path, "wb") as f:
        f.write(kml_str)

    print("KML file created successfully.")

if __name__ == '__main__':
    convert_to_kml()