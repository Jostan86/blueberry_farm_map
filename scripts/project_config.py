import os
import json
import numpy as np

class ProjectConfig:
    def __init__(self):
        self.project_dir = os.path.join('/', 'home', 'jostan', 'OneDrive', 'Docs', 'Grad_school', 'Research', 'code_projects', 'blueberry_farm_map')
        
        self.data_dir = os.path.join(self.project_dir, 'data_map_1')
        # self.data_dir = os.path.join(self.project_dir, 'data_map_2')

        self.points_kml_path = os.path.join(self.data_dir, 'collected_data.kml')

        self.points_json_path = os.path.join(self.data_dir, 'point_coordinates.json')

        self.map_data_json_path = os.path.join(self.data_dir, 'map_data.json')
        self.map_data_shapefile_path = os.path.join(self.data_dir, 'blueberry_farm_map_shapefile', 'blueberry_farm_map')
        self.map_data_kml_path = os.path.join(self.data_dir, 'blueberry_farm_map.kml')

        self.plot_save_path = os.path.join(self.data_dir, 'blueberry_farm_map.png')

        #### Group numbers ####
        self.boundary_row_groups = [1, 5]
        self.inner_row_groups = [2, 3, 4]
        self.post_groups = [6]
        self.debug_groups = [7]
    
    def get_group_name(self, group_num):
        if group_num in self.boundary_row_groups:
            return 'Boundary Row'
        elif group_num in self.inner_row_groups:
            return 'Inner Row'
        elif group_num in self.post_groups:
            return 'Post'
        elif group_num in self.debug_groups:
            return 'Debug'
        else:
            return 'Unknown'
        
    def save_data_to_json(self, data, file_path: str) -> None:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
    def load_points_from_json(self, file_path: str):
        with open(file_path) as f:
            return json.load(f)
    
    def get_map_data(self):
        map_data = self.load_points_from_json(self.map_data_json_path)

        plant_nums = np.array([point['plant_number'] for point in map_data])
        points = np.array([[point['lat'], point['lon']] for point in map_data])
        groups = np.array([point['group'] for point in map_data])

        return points, groups, plant_nums
        