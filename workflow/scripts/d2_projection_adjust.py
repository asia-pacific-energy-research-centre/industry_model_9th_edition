# Adjustment function
# Set working directory to be the project folder 
import os
import re

# Grab relevant functions from 'useful_functions.py'
from useful_functions import modify_trajectory
from useful_functions import generate_smooth_curve

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()

# Interim industry projections
industry_production = pd.read_csv('./data/industry_projections/interim_all_sectors.csv')

# Define years dictionary tp adjust later 
years = [i for i in range(1980, 2101, 1)]

def industry_traj(economy = '01_AUS', 
            sub1sectors = '14_01_mining_and_quarrying', 
            sub2sectors = 'x',
            proj_start_year = 2021,
            shape = 'increase',
            magnitude = 1.5,
            data = industry_production):
    
    # Where to save files
    industry_final = './data/industry_final/{}/'.format(economy)

    if not os.path.isdir(industry_final):
        os.makedirs(industry_final)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy) &
                    (data['sub1sectors'] == sub1sectors) &
                    (data['sub2sectors'] == sub2sectors)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['adj_value'] = np.nan

    # Want to build a new trajectory: up, down, bottom, top, constant
    traj_end = refined_df.loc[proj_start_year, 'value'] * magnitude

    # Generate new trajectory 
    outcome = generate_smooth_curve(num_points = max(years) - proj_start_year + 1, 
                          shape = shape,
                          start_value = refined_df.loc[proj_start_year, 'value'],
                          end_value = traj_end)
    
    print(type(outcome))

    # Isolate time series
    adj_series = refined_df.copy()[['value']].squeeze().to_dict()

    # Now generate modify current trajectory


industry_traj()


def industry_adj(economy = '01_AUS', 
            sub1sectors = '14_01_mining_and_quarrying', 
            sub2sectors = 'x',
            adjustment = True,
            adjust = {},
            proj_start_year = 2021,
            increment = 0.001,
            data = industry_production):

    # Where to save files
    industry_final = './data/industry_final/{}/'.format(economy)

    if not os.path.isdir(industry_final):
        os.makedirs(industry_final)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy) &
                    (data['sub1sectors'] == sub1sectors) &
                    (data['sub2sectors'] == sub2sectors)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['adj_value'] = np.nan
    
    # Refinement to existing trajectory
    if adjustment:
        years_dict = {}
        for year in years:
            years_dict[year] = 1.0

        # Dictionary that stores the increase in the series required (as defined by the manual_adj applied
        # to original series)
        temp_dict = {}

        for year in years_dict.keys():
            if year in adjust:
                years_dict.update([(year, adjust[year])])
            else:
                pass 

            if year in refined_df.index:
                temp_dict[year] = (refined_df.loc[year, 'value'] * years_dict[year]) - refined_df.loc[year, 'value']
                
                refined_df.loc[year, 'adj_value'] = refined_df.loc[year, 'value'] + sum(temp_dict.values())

            else:
                pass

        refined_df = refined_df.copy().reset_index()

    else:
        for year in refined_df.index:
            if year < proj_start_year:
                refined_df.loc[year, 'adj_value'] = refined_df.loc[year, 'value']

            else:
                refined_df.loc[year, 'adj_value'] = refined_df.loc[year - 1, 'adj_value'] * (1 + increment)

        refined_df = refined_df.copy().reset_index()
    
    # Now chart the result
    chart_df = refined_df.copy().melt(id_vars = ['year', 'economy', 'economy_code', 'series', 'units', 'sub1sectors', 'sub2sectors'], 
                                      value_vars = ['value', 'adj_value'], 
                                      value_name = 'production_value')

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                x = 'year',
                y = 'production_value',
                hue = 'variable')

    ax.set(title = economy + ' ' + sub1sectors + ' ' + sub2sectors,
           xlabel = 'Year',
           ylabel = 'Production index (2017 = 100)')

    plt.legend(title = '')

    plt.tight_layout()
    plt.show()

    if sub2sectors == 'x':
        fig.savefig(industry_final + economy + '_' + sub1sectors + '.png')
    elif sub1sectors == '14_03_manufacturing':
        fig.savefig(industry_final + economy + '_' + sub2sectors + '.png')
    else:
        pass
    
    plt.close()

# Test function runs
industry_adj(economy = '05_PRC',
             adjustment = False,
             adjust = {}, 
             increment = -0.01,
             proj_start_year = 2023, 
             sub1sectors = '14_03_manufacturing', 
             sub2sectors = '14_03_01_iron_and_steel') 

industry_adj(economy = '01_AUS', adjust = {2025: 1.15, 2029: 1.25}, adjustment = True, increment = 0.0) 



# CHAT GPT suggestions

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

def generate_smooth_curve(num_points, shape, start_value):
    """
    Generates a smooth curve based on the specified shape.

    Args:
        num_points (int): The number of points to generate in the smooth curve.
        shape (str): The shape of the smooth curve ('increase', 'decrease',
                     'constant', 'peak', or 'bottom').

    Returns:
        numpy.ndarray: The smooth curve values.
    """
    x = np.linspace(start_value, 1, num_points)
    y = np.zeros(num_points)

    if shape == 'increase':
        y = x

    elif shape == 'decrease':
        y = 1 - x

    elif shape == 'constant':
        y = np.ones(num_points)

    elif shape == 'peak':
        y[:num_points//2] = x[:num_points//2]
        y[num_points//2:] = 1 - x[num_points//2:]

    elif shape == 'bottom':
        y[:num_points//2] = 1 - x[:num_points//2]
        y[num_points//2:] = x[num_points//2:]

    f = interp1d(x, y, kind='cubic')
    interpolated_curve = f(np.linspace(0, 1, len(x)))

    return interpolated_curve


num_points = 10
shape = 'decrease'

smooth_curve = generate_smooth_curve(num_points, shape)
print(smooth_curve)

 
