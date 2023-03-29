# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Now run config file
execfile('./config/config_oct2022.py')

# APEC economies
APEC_econcode = pd.read_csv('./data/config/APEC_economies.csv', header = 0, index_col = 0)\
    .squeeze().to_dict()

# Industry sectprs
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

# GDP and population data
macro_apec = pd.read_csv('./data/macro/APEC_GDP_population.csv')

list(industry_sectors.values())
list(macro_apec.variable.unique())

# Want a function that creates a trajectory from historical (eg 2000) to 2100 for all subsectors



# I dont have historical production for subectors for each of the economies
# I could source some of this information
# Potentially a large subset if I given enough time
# For example, if I choose year 2015 as a base year, and construct a tajectory from that base year,
# even including years before that, then the eventual energy data that is provided, I can then use that
# most up to date year as the beginning year and run the trajectory from there.
# For example, if 2021 energy data 
# And projections of 2000 to 2100
# I would make it so the projections and energy data are aligned in 2021
# and grow energy from there based on the projection trajectory
# I would then layer in an annual efficiency improvement
# In terms of looking at energy growth for subsector and historical GDP I want GDP to be outpacing energy 
# growth because of energy efficency causing a divergence   