import shapefile as shp
from project_config import ProjectConfig

def convert_to_shapefile():
    project_config = ProjectConfig()

    points, groups, plant_nums = project_config.get_map_data()

    # Create a new shapefile writer
    w = shp.Writer(project_config.map_data_shapefile_path, shp.POINT)
    # Define the fields in the shapefile
    w.field('bush_number', 'N')
    w.field('group_number', 'N')
    w.field('group_type', 'C')

    for i in range(len(points)):
        latitude, longitude = points[i]
        bush_number = plant_nums[i]
        group_number = groups[i]
        group_type = project_config.get_group_name(group_number)    

        if group_type == 'Post':
            bush_number = None

        w.point(longitude, latitude)
        w.record(bush_number, group_number, group_type) 

    # Save the shapefile
    w.close()

    print("Shapefile created successfully.")

if __name__ == '__main__':
    convert_to_shapefile()