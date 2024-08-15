import numpy as np
import utm
import matplotlib.pyplot as plt
from project_config import ProjectConfig

def convert_to_utm(points: np.ndarray) -> np.ndarray:
    utm_points = np.array([utm.from_latlon(lat, lon)[:2] for lat, lon in points])
    return utm_points

def set_plot_limits(ax: plt.Axes, points: np.ndarray, zero_axes: bool = False):
    x, y = points[:, 0], points[:, 1]

    x_min, x_max = np.min(x), np.max(x)
    y_min, y_max = np.min(y), np.max(y)

    if zero_axes:
        x_max, y_max = x_max - x_min, y_max - y_min
        x_min, y_min = 0, 0

    ax.set_xlim(x_min - 10, x_max + 10)
    ax.set_ylim(y_min - 10, y_max + 10)


def plot_points(points: np.ndarray,
                group: np.ndarray,
                final_map: bool = True,
                plant_nums: np.ndarray = None,
                save_path: str = None,
                show_fig: bool = True,
                zero_axes: bool = True,
                plot_idx: bool = True) -> None:
    
    project_config = ProjectConfig()
    
    points_utm = convert_to_utm(points)

    x, y = points_utm[:, 0], points_utm[:, 1]

    if zero_axes:
        min_x, min_y = np.min(x), np.min(y)
        x = x - min_x
        y = y - min_y
    
    if final_map:
        # set the dpi and figure size
        fig, ax = plt.subplots(dpi=800, figsize=(6, 7))

        post_idxs = np.where(np.isin(group, project_config.post_groups))[0]
        boundary_idxs = np.where(np.isin(group, project_config.boundary_row_groups))[0]
        inner_row_idxs = np.where(np.isin(group, project_config.inner_row_groups))[0]
        
        ax.scatter(x[inner_row_idxs], y[inner_row_idxs], s=0.5, label='Inner Row')
        ax.scatter(x[boundary_idxs], y[boundary_idxs], s=0.5, label='Boundary Row')
        ax.scatter(x[post_idxs], y[post_idxs], s=0.5, label='Post')

        if plant_nums is not None and plot_idx:
            # Plot the idx of each point next to it
            for i, txt in enumerate(plant_nums):
                if group[i] not in [2, 3, 4]:
                    continue
                ax.annotate(txt, (x[i]+0.4, y[i]-0.35), fontsize=1.5)

        # make custom legend and put it outside the plot on the left and make the points larger
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), markerscale=5)

    else:
        fig, ax = plt.subplots(dpi=300, figsize=(2, 4))
        object_idxs = np.where(np.isin(group, project_config.debug_groups))[0]
        background_idxs = np.where(~np.isin(group, project_config.debug_groups))[0]

        ax.scatter(x[object_idxs], y[object_idxs], s=0.5, c='red')
        ax.scatter(x[background_idxs], y[background_idxs], s=0.5, c='black')


    ax.set_xlabel('Easting (m)')
    ax.set_ylabel('Northing (m)')

    ax.set_aspect('equal')

    set_plot_limits(ax, points_utm, zero_axes)
    
    if save_path:
        plt.savefig(save_path)
        
    if show_fig:
        plt.show()

    
def plot_map_data(plot_nums: bool = True) -> None:
    from project_config import ProjectConfig
    project_config = ProjectConfig()

    points, groups, plant_nums= project_config.get_map_data()

    if plot_nums:
        plot_points(points, groups, plant_nums=plant_nums, save_path=project_config.plot_save_path)
    else:
        plot_points(points, groups, plant_nums=None, save_path=project_config.plot_save_path)


if __name__ == '__main__':
    import matplotlib
    matplotlib.use('TkAgg')
    plot_map_data()





