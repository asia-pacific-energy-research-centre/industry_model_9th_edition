# Adjustment function

# Set working directory to be the project folder
import os
import re

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

def industry_adj(economy = '01_AUS', 
            sub1sectors = '14_01_mining_and_quarrying', 
            sub2sectors = 'x',
            adjustment = True,
            proj_start_year = 2021,
            increment = 0.001,
            data = industry_production,
            adjust = dict):

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

        fig, ax = plt.subplots()

        sns.lineplot(data = refined_df,
                    x = 'year',
                    y = 'value', 
                    ax = ax)
        
        sns.lineplot(data = refined_df,
                    x = 'year',
                    y = 'adj_value', 
                    ax = ax)
        
        plt.show()

    else:
        for year in refined_df.index:
            if year < proj_start_year:
                refined_df.loc[year, 'adj_value'] = refined_df.loc[year, 'value']

            else:
                refined_df.loc[year, 'adj_value'] = refined_df.loc[year - 1, 'value'] * (1 + increment)

        refined_df = refined_df.copy().reset_index()

        fig, ax = plt.subplots()

        sns.lineplot(data = refined_df,
                    x = 'year',
                    y = 'value', 
                    ax = ax)
        
        sns.lineplot(data = refined_df,
                    x = 'year',
                    y = 'adj_value', 
                    ax = ax)    

industry_adj(economy = '03_CDA', adjust = {2025: 1.15, 2029: 1.25}, adjustment = True) 
