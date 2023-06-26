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


import numpy as np
from scipy.interpolate import interp1d

def generate_smooth_curve(num_points, shape, start_value, end_value):
    """
    Generates a smooth curve based on the specified shape.

    Args:
        num_points (int): The number of points to generate in the smooth curve.
        shape (str): The shape of the smooth curve ('increase', 'decrease',
                     'constant', 'peak', or 'bottom').

    Returns:
        numpy.ndarray: The smooth curve values.
    """
    x = np.linspace(start_value, end_value, num_points)
    y = np.zeros(num_points)

    if (shape == 'increase') | (shape == 'decrease'):
        y = x

    elif shape == 'constant':
        y = np.linspace(start_value, start_value, num_points)

    elif (shape == 'peak') | (shape == 'bottom'):
        y[:num_points//2] = x[:num_points//2]
        y[num_points//2:] = x[:num_points//2][::-1]

    f = interp1d(x, y, kind = 'cubic')
    interpolated_curve = f(np.linspace(start_value, end_value, len(x)))

    return interpolated_curve