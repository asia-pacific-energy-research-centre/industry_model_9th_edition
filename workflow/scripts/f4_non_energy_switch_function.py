# Non-energy hydrogen (and other fuel) switching
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Modelled years
proj_years = list(range(2021, 2101, 1))

# Also grab historical energy data
hist_egeda = pd.read_csv(latest_EGEDA).loc[:, :'2020']

# Functions for Hydrogen and CCS
# Hydrogen
def hydrogen_ne(start_year = 2030,
                increment = 0.01):
    
    hyd_df = pd.DataFrame()
    
    temp_list = [[i, '16_x_hydrogen', 1.0, (i - start_year + 1) * increment] for i in range(start_year, proj_years[-1] + 1, 1)] 
    temp_df = pd.DataFrame(temp_list)

    hyd_df = pd.concat([hyd_df, temp_df]).copy().reset_index(drop = True)

    hyd_df.columns = ['year', 'fuel', 'fuel_ratio', 'share']

    return hyd_df

# Master function for all fuel switching
def fuel_switch_ne(economy = '01_AUS',
                   base_year = 2021,
                   hydrogen_ref = False,
                   hydrogen_tgt = False,
                   hist_data = hist_egeda,
                   hyd_start_ref = 2040,
                   hyd_start_tgt = 2030,
                   hyd_increment_ref = 0.005,
                   hyd_increment_tgt = 0.01):
    """Function to layer in hydrogen for all APEC economies for non-energy."""

    # Save location for charts and data
    save_location = './results/non_energy/3_fuel_switch/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    # Grab the relevant data to manipulate the fuel shares
    data_ref = pd.read_csv('./results/non_energy/2_nonenergy_projections/{}/{}_non_energy_ref.csv'.format(economy, economy))
    data_tgt = pd.read_csv('./results/non_energy/2_nonenergy_projections/{}/{}_non_energy_tgt.csv'.format(economy, economy))

    # Define fuel ratio data frame for base year (base) and save that for use later
    ne_ratio_ref = data_ref[data_ref['year'] == base_year].copy().reset_index(drop = True)
    ne_ratio_ref = ne_ratio_ref.loc[:, ['fuels', 'energy']].copy()
    base_year_ne = ne_ratio_ref['energy'].sum()

    for i in range(len(data_ref['fuels'].unique())): 
        ne_ratio_ref.iloc[i, 1] = data_ref.iloc[i, -1] / base_year_ne

    ne_ratio_tgt = ne_ratio_ref.copy()

    ne_ratio_ref['year'] = base_year
    ne_ratio_tgt['year'] = base_year

    # REF: Now build in hydrogen switch
    for year in proj_years[1:]:
        if hyd_start_ref > year:
            ratio_nextyear = ne_ratio_ref[ne_ratio_ref['year'] == year - 1].copy()
            ratio_nextyear['year'] = year
            ne_ratio_ref = pd.concat([ne_ratio_ref, ratio_nextyear]).copy().reset_index(drop = True)

        else:    
            ratio_nextyear = ne_ratio_ref[ne_ratio_ref['year'] == year - 1].copy()
            ratio_thisyear = ratio_nextyear.copy()
            ratio_nextyear['year'] = year

            non_zero_ref = list(ratio_nextyear[(ratio_nextyear['energy'] != 0) &
                                               (ratio_nextyear['year'] == year)]['fuels'])
            non_zero_ne_ref = [i for i in non_zero_ref]
    
            for fuel in non_zero_ne_ref:
                if (hyd_increment_ref / (len(non_zero_ne_ref)) >= ratio_thisyear.loc[ratio_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    ratio_nextyear.loc[ratio_nextyear['fuels'] == fuel, 'energy'] = 0

                elif (hyd_increment_ref / (len(non_zero_ne_ref)) < ratio_thisyear.loc[ratio_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    ratio_nextyear.loc[ratio_nextyear['fuels'] == fuel, 'energy'] = ratio_thisyear.loc[ratio_thisyear['fuels'] == fuel, 'energy'].values[0] - \
                        (hyd_increment_ref / (len(non_zero_ne_ref)))
                
            # New value for electricity
            if (1 - ratio_thisyear.loc[ratio_thisyear['fuels'] == '16_others', 'energy'].values[0]) < hyd_increment_ref:
                ratio_nextyear.loc[ratio_nextyear['fuels'] == '16_others', 'energy'] = 1.0 

            elif (1 - ratio_thisyear.loc[ratio_thisyear['fuels'] == '16_others', 'energy'].values[0]) >= hyd_increment_ref:
                ratio_nextyear.loc[ratio_nextyear['fuels'] == '16_others', 'energy'] = ratio_thisyear.loc[ratio_thisyear['fuels'] == '16_others', 'energy'].values[0] + hyd_increment_ref

            ne_ratio_ref = pd.concat([ne_ratio_ref, ratio_nextyear]).copy().reset_index(drop = True)

    # Ensure that the sum of the ratio remains 1 for all years 
    grouped_ref = ne_ratio_ref.groupby('year')

    for year, group in grouped_ref:
        sum_energy = group['energy'].sum()

        if sum_energy != 1:
            group['energy'] = group['energy'] / sum_energy

        ne_ratio_ref.loc[group.index] = group

    # Now use the updated fuel share dataframe to deliver new energy results, that have been electrified
    # Grab total energy by year
    # REF
    total_ref = data_ref.copy().groupby('year').sum()['energy']
    
    for year in proj_years:    
        ne_ratio_ref.loc[ne_ratio_ref['year'] == year, 'new_energy'] = ne_ratio_ref.loc[ne_ratio_ref['year'] == year, 'energy'] * total_ref[year]

    switched_ref = ne_ratio_ref.copy()[['fuels', 'year', 'new_energy']].rename(columns = {'new_energy': 'energy'})
    
    # Create metadata
    switched_ref['scenarios'] = 'reference'
    switched_ref['economy'] = economy
    switched_ref['sectors'] = '17_nonenergy_use'
    switched_ref['sub1sectors'] = 'x'
    switched_ref['subfuels'] = 'x'

    # Organise the dataframe to be saved
    switched_ref = switched_ref[['scenarios', 'economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels', 'year', 'energy']]

fuel_switch_ne(economy = '19_THA', hydrogen_ref = True)

