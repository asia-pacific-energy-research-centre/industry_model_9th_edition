# Adjustment function
# Set working directory to be the project folder 
import os
import re

# Grab relevant functions from 'useful_functions.py'
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
industry_production = pd.read_csv('./data/industry_production/3_industry_projections/interim_all_sectors.csv')

# Interim nonenergy projections
nonenergy_production = pd.read_csv('./data/non_energy/1_nonenergy_projections/interim_all_sectors.csv')

if os.path.isfile('./data/non_energy/2_nonenergy_refine1/refined_nonenergy_all.csv'):
    nonenergy_refine = pd.read_csv('./data/non_energy/2_nonenergy_refine1/refined_nonenergy_all.csv')
else:
    nonenergy_refine = pd.read_csv('./data/non_energy/1_nonenergy_projections/interim_all_sectors.csv')


# Define years list tp adjust later 
years = [i for i in range(1980, 2101, 1)]

# Function definition to override modelled trajectory

def industry_traj(economy = '01_AUS', 
            sub1sectors = '14_01_mining_and_quarrying', 
            sub2sectors = 'x',
            proj_start_year = 2021,
            shape = 'increase',
            magnitude = 1.5,
            apex_mag = 1.5,
            apex_loc = 10,
            data = industry_production):
    
    # Where to save files
    industry_refine1 = './data/industry_production/4_industry_refine1/{}/'.format(economy)

    if not os.path.isdir(industry_refine1):
        os.makedirs(industry_refine1)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy) &
                    (data['sub1sectors'] == sub1sectors) &
                    (data['sub2sectors'] == sub2sectors)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['adj_value'] = np.nan

    # Want to build a new trajectory: up, down, bottom, top, constant
    traj_start = refined_df.loc[proj_start_year, 'value'] 
    traj_end = refined_df.loc[proj_start_year, 'value'] * magnitude
    apex = apex_mag * traj_end
    
    # Generate new trajectory 
    outcome = generate_smooth_curve(num_points = max(years) - proj_start_year + 1, 
                                    shape = shape,
                                    start_value = traj_start,
                                    end_value = traj_end,
                                    apex_point = apex,
                                    apex_position = apex_loc)
    
    outcome_df = pd.DataFrame(outcome, index = range(proj_start_year, max(refined_df.index) + 1))

    # Populate the adj_value column in refined_df
    
    for year in refined_df.index:
        if year < proj_start_year:
            refined_df.loc[year, 'adj_value'] = refined_df.loc[year, 'value']
        elif year >= proj_start_year:
            refined_df.loc[year, 'adj_value'] = outcome_df.loc[year, 0] 

    # Reset index
    refined_df = refined_df.copy().reset_index()

    # Now generate charts
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
           ylabel = 'Production index (2017 = 100)',
           ylim = (0, chart_df['production_value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout() 
    plt.show()

    if sub2sectors == 'x':
        fig.savefig(industry_refine1 + economy + '_' + sub1sectors + '.png')
    elif sub1sectors == '14_03_manufacturing':
        fig.savefig(industry_refine1 + economy + '_' + sub2sectors + '.png')
    else:
        pass
    
    plt.close()

    adj_data = refined_df.copy()[['economy', 'economy_code', 'series', 'year', 'units', 'sub1sectors', 'sub2sectors', 'adj_value']]\
        .rename(columns = {'adj_value': 'value'})
    
    if sub2sectors == 'x':
        adj_data.to_csv(industry_refine1 + economy + '_' + sub1sectors + '.csv', index = False)
    elif sub1sectors == '14_03_manufacturing':
        adj_data.to_csv(industry_refine1 + economy + '_' + sub2sectors + '.csv', index = False)
    else:
        pass

##########################################################################################################
# Manual adjustment function

def industry_adj(economy = '01_AUS', 
            sub1sectors = '14_01_mining_and_quarrying', 
            sub2sectors = 'x',
            adjust = {},
            data = industry_production):

    # Where to save files
    industry_refine2 = './data/industry_production/5_industry_refine2/{}/'.format(economy)

    if not os.path.isdir(industry_refine2):
        os.makedirs(industry_refine2)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy) &
                    (data['sub1sectors'] == sub1sectors) &
                    (data['sub2sectors'] == sub2sectors)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['adj_value'] = np.nan
    
    # Refinement to existing trajectory
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
           ylabel = 'Production index (2017 = 100)',
           ylim = (0, chart_df['production_value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout()
    plt.show()

    if sub2sectors == 'x':
        fig.savefig(industry_refine2 + economy + '_' + sub1sectors + '.png')
    elif sub1sectors == '14_03_manufacturing':
        fig.savefig(industry_refine2 + economy + '_' + sub2sectors + '.png')
    else:
        pass
    
    plt.close()

    adj_data = refined_df.copy()[['economy', 'economy_code', 'series', 'year', 'units', 'sub1sectors', 'sub2sectors', 'adj_value']]\
        .rename(columns = {'adj_value': 'value'})
    
    if sub2sectors == 'x':
        adj_data.to_csv(industry_refine2 + economy + '_' + sub1sectors + '.csv', index = False)
    elif sub1sectors == '14_03_manufacturing':
        adj_data.to_csv(industry_refine2 + economy + '_' + sub2sectors + '.csv', index = False)
    else:
        pass

# Define function that creates trajectories for target scenario

def scenario_adj(economy = '01_AUS', 
                 sub1sectors = '14_01_mining_and_quarrying', 
                 sub2sectors = 'x',
                 increment = 0.01,
                 start_year = 2021,
                 end_year = 2040,
                 data = industry_production):
    
    # Where to save files
    industry_scenarios = './data/industry_production/6_industry_scenarios/{}/'.format(economy)

    if not os.path.isdir(industry_scenarios):
        os.makedirs(industry_scenarios)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy) &
                    (data['sub1sectors'] == sub1sectors) &
                    (data['sub2sectors'] == sub2sectors)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['tgt_value'] = refined_df['value']

    for year in refined_df.index:
        if (year >= start_year) & (year <= end_year):
            growth_factor = (1 + increment) ** (year - start_year)
            refined_df.loc[year, 'tgt_value'] = refined_df.loc[year, 'value'] * growth_factor

        elif year > end_year:
            refined_df.loc[year, 'tgt_value'] = refined_df.loc[year - 1, 'tgt_value'] + (refined_df.loc[year, 'value'] - refined_df.loc[year - 1, 'value'])

        elif year < start_year:
            refined_df.loc[year, 'tgt_value'] = refined_df.loc[year, 'value']

        else:
            pass

    refined_df = refined_df.copy().reset_index()

    # Now chart the result
    chart_df = refined_df.copy().melt(id_vars = ['year', 'economy', 'economy_code', 'series', 'units', 'sub1sectors', 'sub2sectors'], 
                                      value_vars = ['value', 'tgt_value'], 
                                      value_name = 'production_value')

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                x = 'year',
                y = 'production_value',
                hue = 'variable')

    ax.set(title = economy + ' ' + sub1sectors + ' ' + sub2sectors,
           xlabel = 'Year',
           ylabel = 'Production index (2017 = 100)',
           ylim = (0, chart_df['production_value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout()
    plt.show()

    if sub2sectors == 'x':
        fig.savefig(industry_scenarios + economy + '_' + sub1sectors + '.png')
    elif sub1sectors == '14_03_manufacturing':
        fig.savefig(industry_scenarios + economy + '_' + sub2sectors + '.png')
    else:
        pass
    
    plt.close()

    adj_data = refined_df.copy()[['economy', 'economy_code', 'series', 'year', 'units', 'sub1sectors', 'sub2sectors', 'tgt_value']]\
        .rename(columns = {'tgt_value': 'value'})
    
    if sub2sectors == 'x':
        adj_data.to_csv(industry_scenarios + economy + '_' + sub1sectors + '.csv', index = False)
    elif sub1sectors == '14_03_manufacturing':
        adj_data.to_csv(industry_scenarios + economy + '_' + sub2sectors + '.csv', index = False)
    else:
        pass

######################################################################################################################

def nonenergy_traj(economy = '01_AUS', 
                   proj_start_year = 2021,
                   shape = 'increase',
                   magnitude = 1.5,
                   apex_mag = 1.5,
                   apex_loc = 10,
                   data = nonenergy_production):
    
    # Where to save files
    nonenergy_refine1 = './data/non_energy/2_nonenergy_refine1/{}/'.format(economy)

    if not os.path.isdir(nonenergy_refine1):
        os.makedirs(nonenergy_refine1)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['adj_value'] = np.nan

    # Want to build a new trajectory: up, down, bottom, top, constant
    traj_start = refined_df.loc[proj_start_year, 'value'] 
    traj_end = refined_df.loc[proj_start_year, 'value'] * magnitude
    apex = apex_mag * traj_end
    
    # Generate new trajectory 
    outcome = generate_smooth_curve(num_points = max(years) - proj_start_year + 1, 
                                    shape = shape,
                                    start_value = traj_start,
                                    end_value = traj_end,
                                    apex_point = apex,
                                    apex_position = apex_loc)
    
    outcome_df = pd.DataFrame(outcome, index = range(proj_start_year, max(refined_df.index) + 1))

    # Populate the adj_value column in refined_df
    
    for year in refined_df.index:
        if year < proj_start_year:
            refined_df.loc[year, 'adj_value'] = refined_df.loc[year, 'value']
        elif year >= proj_start_year:
            refined_df.loc[year, 'adj_value'] = outcome_df.loc[year, 0] 

    # Reset index
    refined_df = refined_df.copy().reset_index()

    # Now generate charts
    chart_df = refined_df.copy().melt(id_vars = ['year', 'economy', 'economy_code', 'series', 'units', 'sectors', 'sub1sectors'], 
                                      value_vars = ['value', 'adj_value'], 
                                      value_name = 'production_value')

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                x = 'year',
                y = 'production_value',
                hue = 'variable')

    ax.set(title = economy + ' non-energy use',
           xlabel = 'Year',
           ylabel = 'Production index (2017 = 100)',
           ylim = (0, chart_df['production_value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout() 
    plt.show()

    fig.savefig(nonenergy_refine1 + economy + '_non_energy.png')
    
    plt.close()

    adj_data = refined_df.copy()[['economy', 'economy_code', 'series', 'year', 'units', 'sectors', 'sub1sectors', 'adj_value']]\
        .rename(columns = {'adj_value': 'value'})
    
    adj_data.to_csv(nonenergy_refine1 + economy + '_non_energy.csv', index = False)

##########################################################################################################

def nonenergy_adj(economy = '01_AUS', 
                  adjust = {},
                  data = nonenergy_refine):

    # Where to save files
    nonenergy_refine2 = './data/non_energy/3_nonenergy_refine2/{}/'.format(economy)

    if not os.path.isdir(nonenergy_refine2):
        os.makedirs(nonenergy_refine2)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['adj_value'] = np.nan
    
    # Refinement to existing trajectory
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
    
    # Now chart the result
    chart_df = refined_df.copy().melt(id_vars = ['year', 'economy', 'economy_code', 'series', 'units', 'sectors', 'sub1sectors'], 
                                      value_vars = ['value', 'adj_value'], 
                                      value_name = 'production_value')

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                x = 'year',
                y = 'production_value',
                hue = 'variable')

    ax.set(title = economy + ' non-energy use',
           xlabel = 'Year',
           ylabel = 'Production index (2017 = 100)',
           ylim = (0, chart_df['production_value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout()
    plt.show()

    fig.savefig(nonenergy_refine2 + economy + '_non_energy.png')
    
    plt.close()

    adj_data = refined_df.copy()[['economy', 'economy_code', 'series', 'year', 'units', 'sectors', 'sub1sectors', 'adj_value']]\
        .rename(columns = {'adj_value': 'value'})

    adj_data.to_csv(nonenergy_refine2 + economy + '_non_energy.csv', index = False)

##############################################################################################################################

def scenario_adj_ne(economy = '01_AUS', 
                   increment = 0.01,
                   start_year = 2021,
                   end_year = 2040,
                   data = industry_production):
    
    # Where to save files
    nonenergy_scenarios = './data/non_energy/4_nonenergy_scenarios/{}/'.format(economy)

    if not os.path.isdir(nonenergy_scenarios):
        os.makedirs(nonenergy_scenarios)
    
    # Relevant dataframe grab
    refined_df = data[(data['economy_code'] == economy)].copy().reset_index(drop = True)
    
    # Set year as index
    refined_df = refined_df.set_index('year')
    # Updated column with refined estimates
    refined_df['tgt_value'] = refined_df['value']

    for year in refined_df.index:
        if (year >= start_year) & (year <= end_year):
            growth_factor = (1 + increment) ** (year - start_year)
            refined_df.loc[year, 'tgt_value'] = refined_df.loc[year, 'value'] * growth_factor

        elif year > end_year:
            refined_df.loc[year, 'tgt_value'] = refined_df.loc[year - 1, 'tgt_value'] + (refined_df.loc[year, 'value'] - refined_df.loc[year - 1, 'value'])

        elif year < start_year:
            refined_df.loc[year, 'tgt_value'] = refined_df.loc[year, 'value']

        else:
            pass

    refined_df = refined_df.copy().reset_index()

    # Now chart the result
    chart_df = refined_df.copy().melt(id_vars = ['year', 'economy', 'economy_code', 'series', 'units', 'sectors', 'sub1sectors'], 
                                      value_vars = ['value', 'tgt_value'], 
                                      value_name = 'production_value')

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                x = 'year',
                y = 'production_value',
                hue = 'variable')

    ax.set(title = economy + ' non-energy use',
           xlabel = 'Year',
           ylabel = 'Production index (2017 = 100)',
           ylim = (0, chart_df['production_value'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout()
    plt.show()
    
    fig.savefig(nonenergy_scenarios + economy + '_non_energy.png')
    
    plt.close()

    adj_data = refined_df.copy()[['economy', 'economy_code', 'series', 'year', 'units', 'sectors', 'sub1sectors', 'tgt_value']]\
        .rename(columns = {'tgt_value': 'value'})
    
    adj_data.to_csv(nonenergy_scenarios + economy + '_non_energy.csv', index = False) 