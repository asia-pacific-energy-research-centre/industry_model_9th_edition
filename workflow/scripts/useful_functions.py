# Useful functions

def modify_trajectory(time_series, chosen_year, new_trajectory):
    """
    Modifies the trajectory from a chosen year in the annual time series.

    Args:
        time_series (dict): The original annual time series.
        chosen_year (int): The year to overwrite the trajectory.
        new_trajectory (list): The new trajectory shape to replace the chosen year.

    Returns:
        dict: The modified annual time series with the new trajectory shape.
    """
    modified_series = {}

    for year, value in time_series.items():
        if year < chosen_year:
            modified_series[year] = value
        elif year == chosen_year:
            modified_series[year] = value
        else:
            modified_series[year] = new_trajectory.pop(0)

    return modified_series


# import numpy as np
# from scipy.interpolate import interp1d

# def generate_smooth_curve(num_points, shape, start_value, end_value, apex_point = None, apex_position = None):
#     """
#     Generates a smooth curve based on the specified shape.

#     Args:
#         num_points (int): The number of points to generate in the smooth curve.
#         shape (str): The shape of the smooth curve ('increase', 'decrease',
#                      'constant', 'peak', or 'bottom').
#         start_value (float): The starting value of the curve.
#         end_value (float): The ending value of the curve.
#         apex_point (float, optional): The position of the apex along the x-axis.
#                                      Only applicable for 'peak' or 'bottom' shapes.

#     Returns:
#         numpy.ndarray: The smooth curve values.
#     """
#     if shape == 'constant':
#         return np.full(num_points, start_value)

#     x = np.linspace(start_value, end_value, num_points)
#     y = np.zeros(num_points)

#     if shape == 'increase':
#         y = start_value + (end_value - start_value) * ((x - start_value) / (end_value - start_value)) ** 2

#     elif shape == 'decrease':
#         y = end_value - (end_value - start_value) * ((end_value - x) / (end_value - start_value)) ** 2

#     elif shape == 'peak' or shape == 'bottom':
#         if apex_point is None:
#             raise ValueError("Apex point must be specified for 'peak' or 'bottom' shapes.")
        
#         if apex_position is None:
#             apex_position = 0.5 # Default

#         if apex_position < 0 or apex_position > 1:
#             raise ValueError("Apex position must be between 0 and 1.")
        
#         apex_x = start_value + (end_value - start_value) * apex_position

#         x_left = np.linspace(start_value, apex_x, int(num_points * apex_position) + 1)
#         x_right = np.linspace(apex_x, end_value, num_points - int(num_points * apex_position))
#         y_left = apex_point - (apex_point - start_value) * ((apex_x - x_left) / (apex_x - start_value)) ** 2
#         y_right = apex_point + (end_value - apex_point) * ((x_right - apex_x) / (end_value - apex_x)) ** 2
#         y[:int(num_points * apex_position) + 1] = y_left
#         y[int(num_points * apex_position) + 1:] = y_right

#     else:
#         raise ValueError("Invalid shape. Supported shapes are 'increase', 'decrease', 'constant', 'peak', or 'bottom'.")

#     f = interp1d(x, y, kind = 'quadratic')
#     interpolated_curve = f(np.linspace(start_value, end_value, num_points))

#     return interpolated_curve

import numpy as np
from scipy.interpolate import interp1d

def generate_smooth_curve(num_points, shape, start_value, end_value, apex_point = None):
    """
    Generates a smooth curve based on the specified shape.

    Args:
        num_points (int): The number of points to generate in the smooth curve.
        shape (str): The shape of the smooth curve ('increase', 'decrease',
                     'constant', 'peak', or 'bottom').
        start_value (float): The starting value of the curve.
        end_value (float): The ending value of the curve.
        apex_point (float, optional): The position of the apex along the x-axis.
                                     Only applicable for 'peak' or 'bottom' shapes.

    Returns:
        numpy.ndarray: The smooth curve values.
    """
    if shape == 'constant':
        return np.full(num_points, start_value)

    x = np.linspace(start_value, end_value, num_points)
    y = np.zeros(num_points)

    if shape == 'increase':
        y = start_value + (end_value - start_value) * ((x - start_value) / (end_value - start_value)) ** 2

    elif shape == 'decrease':
        y = end_value - (end_value - start_value) * ((end_value - x) / (end_value - start_value)) ** 2

    elif shape == 'peak' or shape == 'bottom':
        if apex_point is None:
            raise ValueError("Apex point must be specified for 'peak' or 'bottom' shapes.")
        # HUUUUUH
        apex_index = int((apex_point - start_value) / (end_value - start_value) * num_points)

        x_left = np.linspace(start_value, apex_point, num_points // 2)
        x_right = np.linspace(apex_point, end_value, num_points - num_points // 2)
        y_left = apex_point - (apex_point - start_value) * ((apex_point - x_left) / (apex_point - start_value)) ** 2
        y_right = apex_point + (end_value - apex_point) * ((x_right - apex_point) / (end_value - apex_point)) ** 2
        y[:num_points // 2] = y_left
        y[num_points // 2:] = y_right

    else:
        raise ValueError("Invalid shape. Supported shapes are 'increase', 'decrease', 'constant', 'peak', or 'bottom'.")

    f = interp1d(x, y, kind = 'quadratic')
    interpolated_curve = f(np.linspace(start_value, end_value, num_points))

    return interpolated_curve

# import numpy as np
# from scipy.interpolate import interp1d

# def generate_smooth_curve(num_points, shape, start_value, end_value, apex_point=None, apex_position=None):
#     """
#     Generates a smooth curve based on the specified shape.

#     Args:
#         num_points (int): The number of points to generate in the smooth curve.
#         shape (str): The shape of the smooth curve ('increase', 'decrease',
#                      'constant', 'peak', or 'bottom').
#         start_value (float): The starting value of the curve.
#         end_value (float): The ending value of the curve.
#         apex_point (float, optional): The position of the apex along the x-axis.
#                                      Only applicable for 'peak' or 'bottom' shapes.

#     Returns:
#         numpy.ndarray: The smooth curve values.
#     """
#     if shape == 'constant':
#         return np.full(num_points, start_value)

#     x = np.linspace(start_value, end_value, num_points)
#     y = np.zeros(num_points)

#     if shape == 'increase':
#         y = start_value + (end_value - start_value) * ((x - start_value) / (end_value - start_value)) ** 2

#     elif shape == 'decrease':
#         y = end_value - (end_value - start_value) * ((end_value - x) / (end_value - start_value)) ** 2

#     elif shape == 'peak' or shape == 'bottom':
#         if apex_point is None:
#             raise ValueError("Apex point must be specified for 'peak' or 'bottom' shapes.")

#         if apex_position is None:
#             apex_position = 0.5  # Default

#         if apex_position < 0 or apex_position > 1:
#             raise ValueError("Apex position must be between 0 and 1.")

#         apex_x = start_value + (end_value - start_value) * apex_position

#         x_left = np.linspace(start_value, apex_x, int(num_points * apex_position) + 1)
#         x_right = np.linspace(apex_x, end_value, num_points - int(num_points * apex_position))
#         y_left = apex_point - (apex_point - start_value) * ((apex_x - x_left) / (apex_x - start_value)) ** 2
#         y_right = apex_point + (end_value - apex_point) * ((x_right - apex_x) / (end_value - apex_x)) ** 2
#         y[:int(num_points * apex_position) + 1] = y_left
#         y[int(num_points * apex_position) + 1:] = y_right

#     else:
#         raise ValueError("Invalid shape. Supported shapes are 'increase', 'decrease', 'constant', 'peak', or 'bottom'.")

#     f = interp1d(x, y, kind='quadratic')
#     interpolated_curve = f(np.linspace(start_value, end_value, num_points))

#     return interpolated_curve

