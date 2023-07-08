# Fuel switching
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Modelled years
proj_years = list(range(2021, 2101, 1))

# Also grab historical energy data
hist_egeda = pd.read_csv(latest_EGEDA).loc[:, :'2020']

# don't electrify
no_elec = ['12_solar', '17_electricity', '18_heat']

# biomass 
no_biomass = ['12_solar', '15_solid_biomass', '17_electricity', '18_heat']

# To gas (from coal)
to_gas = ['06_crude_oil_and_ngl', '07_petroleum_products', '08_gas', '12_solar', '15_solid_biomass',
          '16_others', '17_electricity', '18_heat']

# Functions for Hydrogen and CCS
# Hydrogen
def hydrogen(fuel_mix = {'16_x_hydrogen': 0.5,
                         '17_electricity': 0.5},
             start_year = 2030,
             increment = 0.01):
    
    hyd_df = pd.DataFrame()
    
    for j, (fuel, share) in enumerate(fuel_mix.items()):
        temp_list = [[i, fuel, share, (i - start_year + 1) * increment] for i in range(start_year, proj_years[-1] + 1, 1)] 
        temp_df = pd.DataFrame(temp_list)

        hyd_df = pd.concat([hyd_df, temp_df]).copy().reset_index(drop = True)

    hyd_df.columns = ['year', 'fuel', 'fuel_ratio', 'share']

    return hyd_df

# Master function for all fuel switching
def fuel_switch(economy = '01_AUS',
                sector = ind1[0],
                base_year = 2021,
                hist_data = hist_egeda,
                elec_start_ref = 2021,
                elec_rate_ref = 0.005,
                elec_start_tgt = 2021,
                elec_rate_tgt = 0.0075,
                bio_start_ref = 2021,
                bio_rate_ref = 0.0,
                bio_start_tgt = 2021,
                bio_rate_tgt = 0.0,
                c2g_start_ref = 2025,
                c2g_rate_ref = 0.0,
                c2g_start_tgt = 2025,
                c2g_rate_tgt = 0.0,
                hydrogen_ref = False,
                hydrogen_tgt = False,
                hyd_fuel_mix = {'16_x_hydrogen': 0.5,
                                '17_electricity': 0.5},
                hyd_start_ref = 2040,
                hyd_start_tgt = 2030,
                hyd_increment_ref = 0.005,
                hyd_increment_tgt = 0.01,
                ccs_ref = False,
                ccs_tgt = False,
                ccs_start_ref = 2040,
                ccs_start_tgt = 2030,
                ccs_increment_ref = 0.01,
                ccs_increment_tgt = 0.01):
    
    # Save location for charts and data
    save_location = './results/industry/3_fuel_switch/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    hyd_ccs_location = save_location + 'hydrogen_ccs/'

    if not os.path.isdir(hyd_ccs_location):
        os.makedirs(hyd_ccs_location)

    # Grab the relevant data to manipulate the fuel shares
    data_ref = pd.read_csv('./results/industry/2_energy_projections/{}/{}_{}_energy_ref.csv'.format(economy, economy, sector))
    data_tgt = pd.read_csv('./results/industry/2_energy_projections/{}/{}_{}_energy_tgt.csv'.format(economy, economy, sector))

    # Define fuel ratio data frame for base year (base) and save that for use later
    fuel_ratio_ref = data_ref[data_ref['year'] == base_year].copy().reset_index(drop = True)
    fuel_ratio_ref = fuel_ratio_ref.loc[:, ['fuels', 'energy']].copy()
    base_year_energy = fuel_ratio_ref['energy'].sum()
    
    for i in range(len(data_ref['fuels'].unique())): 
        fuel_ratio_ref.iloc[i, 1] = data_ref.iloc[i, -1] / base_year_energy

    fuel_ratio_tgt = fuel_ratio_ref.copy()

    fuel_ratio_ref['year'] = base_year
    fuel_ratio_tgt['year'] = base_year

    ############################################################################################################################
    # REF: Now build in the electrification, whereby electricity takes share from the electrifiable fuels (those not in no_elec)
    for year in proj_years[1:]:
        if elec_start_ref > year:
            fr_nextyear = fuel_ratio_ref[fuel_ratio_ref['year'] == year - 1].copy()
            fr_nextyear['year'] = year
            fuel_ratio_ref = pd.concat([fuel_ratio_ref, fr_nextyear]).copy().reset_index(drop = True)

        else:    
            fr_nextyear = fuel_ratio_ref[fuel_ratio_ref['year'] == year - 1].copy()
            fr_thisyear = fr_nextyear.copy()
            fr_nextyear['year'] = year

            non_zero_ref = list(fr_nextyear[(fr_nextyear['energy'] != 0) &
                                            (fr_nextyear['year'] == year)]['fuels'])
            non_zero_fuels_ref = [i for i in non_zero_ref if i not in no_elec]
    
            for fuel in non_zero_fuels_ref:
                if (elec_rate_ref / (len(non_zero_fuels_ref)) >= fr_thisyear.loc[fr_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    fr_nextyear.loc[fr_nextyear['fuels'] == fuel, 'energy'] = 0

                elif (elec_rate_ref / (len(non_zero_fuels_ref)) < fr_thisyear.loc[fr_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    fr_nextyear.loc[fr_nextyear['fuels'] == fuel, 'energy'] = fr_thisyear.loc[fr_thisyear['fuels'] == fuel, 'energy'].values[0] - \
                        (elec_rate_ref / (len(non_zero_fuels_ref)))
                
            # New value for electricity
            if (1 - fr_thisyear.loc[fr_thisyear['fuels'] == '17_electricity', 'energy'].values[0]) < elec_rate_ref:
                fr_nextyear.loc[fr_nextyear['fuels'] == '17_electricity', 'energy'] = 1.0 

            elif (1 - fr_thisyear.loc[fr_thisyear['fuels'] == '17_electricity', 'energy'].values[0]) >= elec_rate_ref:
                fr_nextyear.loc[fr_nextyear['fuels'] == '17_electricity', 'energy'] = fr_thisyear.loc[fr_thisyear['fuels'] == '17_electricity', 'energy'].values[0] + elec_rate_ref

            fuel_ratio_ref = pd.concat([fuel_ratio_ref, fr_nextyear]).copy().reset_index(drop = True)
        
    ##############################################################################################################################
    # TGT: build in electrification, whereby electricity takes share from the electrifiable fuels (those not in no_elec)
    for year in proj_years[1:]:
        if elec_start_tgt > year:
            fr_nextyear = fuel_ratio_tgt[fuel_ratio_tgt['year'] == year - 1].copy()
            fr_nextyear['year'] = year
            fuel_ratio_tgt = pd.concat([fuel_ratio_tgt, fr_nextyear]).copy().reset_index(drop = True)

        else:
            fr_nextyear = fuel_ratio_tgt[fuel_ratio_tgt['year'] == year - 1].copy()
            fr_thisyear = fr_nextyear.copy()
            fr_nextyear['year'] = year

            non_zero_tgt = list(fr_nextyear[(fr_nextyear['energy'] != 0) &
                                            (fr_nextyear['year'] == year)]['fuels'])
            non_zero_fuels_tgt = [i for i in non_zero_tgt if i not in no_elec]
    
            for fuel in non_zero_fuels_tgt:
                if (elec_rate_tgt / (len(non_zero_fuels_tgt)) >= fr_thisyear.loc[fr_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    fr_nextyear.loc[fr_nextyear['fuels'] == fuel, 'energy'] = 0

                elif (elec_rate_tgt / (len(non_zero_fuels_tgt)) < fr_thisyear.loc[fr_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    fr_nextyear.loc[fr_nextyear['fuels'] == fuel, 'energy'] = fr_thisyear.loc[fr_thisyear['fuels'] == fuel, 'energy'].values[0] - \
                        (elec_rate_tgt / (len(non_zero_fuels_tgt)))
                
            # New value for electricity
            if (1 - fr_thisyear.loc[fr_thisyear['fuels'] == '17_electricity', 'energy'].values[0]) < elec_rate_tgt:
                fr_nextyear.loc[fr_nextyear['fuels'] == '17_electricity', 'energy'] = 1.0 

            elif (1 - fr_thisyear.loc[fr_thisyear['fuels'] == '17_electricity', 'energy'].values[0]) >= elec_rate_tgt:
                fr_nextyear.loc[fr_nextyear['fuels'] == '17_electricity', 'energy'] = fr_thisyear.loc[fr_thisyear['fuels'] == '17_electricity', 'energy'].values[0] + elec_rate_tgt

            fuel_ratio_tgt = pd.concat([fuel_ratio_tgt, fr_nextyear]).copy().reset_index(drop = True)
        
    ################################################################################################################################
    # REF: Now layer in biomass switch
    year_ref = proj_years[0]

    while year_ref < bio_start_ref:
        year_ref += 1

    else:
        # Establish fuels that will be subject to updated value    
        non_zero = list(fuel_ratio_ref[(fuel_ratio_ref['energy'] != 0) & 
                                       (fuel_ratio_ref['year'] == year_ref)]['fuels'])
        bio_update_ref = [z for z in non_zero if z not in no_biomass]
        if len(bio_update_ref) > 0:
            delta_bio = bio_rate_ref / len(bio_update_ref)
        else:
            delta_bio = bio_rate_ref

        for year in range(year_ref, proj_years[-1] + 1, 1):
            for fuel in bio_update_ref:
                fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == fuel), 'energy'] = \
                max(0, fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == fuel), 'energy'].values[0] - ((year - year_ref) * delta_bio))
            
            fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == '15_solid_biomass'), 'energy'] = \
            min(fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year_ref) & (fuel_ratio_ref['fuels'].isin(non_zero)), 'energy'].sum(), 
                fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == '15_solid_biomass'), 'energy'].values[0] + ((year - year_ref) * bio_rate_ref))

    # TGT: Same biomass deal 
    year_tgt = proj_years[0]

    while year_tgt < bio_start_tgt:
        year_tgt += 1

    else:
        # Establish fuels that will be subject to updated value    
        non_zero = list(fuel_ratio_tgt[(fuel_ratio_tgt['energy'] != 0) & 
                                       (fuel_ratio_tgt['year'] == year_tgt)]['fuels'])
        bio_update_tgt = [z for z in non_zero if z not in no_biomass]
        if len(bio_update_tgt) > 0:
            delta_bio = bio_rate_tgt / len(bio_update_tgt)
        else:
            delta_bio = bio_rate_tgt

        for year in range(year_tgt, proj_years[-1] + 1, 1):
            for fuel in bio_update_tgt:
                fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == fuel), 'energy'] = \
                max(0, fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == fuel), 'energy'].values[0] - ((year - year_tgt) * delta_bio))
                
            fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == '15_solid_biomass'), 'energy'] = \
            min(fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year_tgt) & (fuel_ratio_tgt['fuels'].isin(non_zero)), 'energy'].sum(), 
                fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == '15_solid_biomass'), 'energy'].values[0] + ((year - year_tgt) * bio_rate_tgt))
    
    ###########################################################################################################################################
    # Coal to gas
    # REF
    year_ref = proj_years[0]

    while year_ref < c2g_start_ref:
        year_ref += 1

    else:
        # Establish fuels that will be subject to updated value    
        non_zero = list(fuel_ratio_ref[(fuel_ratio_ref['energy'] != 0) & 
                                       (fuel_ratio_ref['year'] == year_ref)]['fuels'])
        
        c2g_update_ref = [k for k in non_zero if k not in to_gas]
        if len(c2g_update_ref) > 0:
            delta_c2g = c2g_rate_ref / len(c2g_update_ref)
        else:
            delta_c2g = c2g_rate_ref

        for year in range(year_ref, proj_years[-1] + 1, 1):
            for fuel in c2g_update_ref:
                fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == fuel), 'energy'] = \
                max(0, fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == fuel), 'energy'].values[0] - ((year - year_ref) * delta_c2g))
            
            fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == '08_gas'), 'energy'] = \
            min(fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year_ref) & (fuel_ratio_ref['fuels'].isin(non_zero)), 'energy'].sum(), 
                fuel_ratio_ref.loc[(fuel_ratio_ref['year'] == year) & (fuel_ratio_ref['fuels'] == '08_gas'), 'energy'].values[0] + ((year - year_ref) * c2g_rate_ref))
            
    # TGT
    year_tgt = proj_years[0]

    while year_tgt < c2g_start_tgt:
        year_tgt += 1

    else:
        # Establish fuels that will be subject to updated value    
        non_zero = list(fuel_ratio_tgt[(fuel_ratio_tgt['energy'] != 0) & 
                                       (fuel_ratio_tgt['year'] == year_tgt)]['fuels'])
        c2g_update_tgt = [k for k in non_zero if k not in to_gas]
        if len(c2g_update_tgt) > 0:
            delta_c2g = c2g_rate_tgt / len(c2g_update_tgt)
        else:
            delta_c2g = c2g_rate_tgt

        for year in range(year_tgt, proj_years[-1] + 1, 1):
            for fuel in c2g_update_tgt:
                fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == fuel), 'energy'] = \
                max(0, fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == fuel), 'energy'].values[0] - ((year - year_tgt) * delta_c2g))
            
            fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == '08_gas'), 'energy'] = \
            min(fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year_tgt) & (fuel_ratio_tgt['fuels'].isin(non_zero)), 'energy'].sum(), 
                fuel_ratio_tgt.loc[(fuel_ratio_tgt['year'] == year) & (fuel_ratio_tgt['fuels'] == '08_gas'), 'energy'].values[0] + ((year - year_tgt) * c2g_rate_tgt))        
    
    ###########################################################################################################################################
    # Ensure that the sum of the ratio remains 1 for all years 
    grouped_ref = fuel_ratio_ref.groupby('year')

    for year, group in grouped_ref:
        sum_energy = group['energy'].sum()

        if sum_energy != 1:
            group['energy'] = group['energy'] / sum_energy

        fuel_ratio_ref.loc[group.index] = group

    grouped_tgt = fuel_ratio_tgt.groupby('year')

    for year, group in grouped_tgt:
        sum_energy = group['energy'].sum()

        if sum_energy != 1:
            group['energy'] = group['energy'] / sum_energy

        fuel_ratio_tgt.loc[group.index] = group    

    ###########################################################################################################################################
    # Now use the updated fuel share dataframe to deliver new energy results, that have been electrified
    # Grab total energy by year
    # REF
    total_ref = data_ref.copy().groupby('year').sum()['energy']
    
    for year in proj_years:    
        fuel_ratio_ref.loc[fuel_ratio_ref['year'] == year, 'new_energy'] = fuel_ratio_ref.loc[fuel_ratio_ref['year'] == year, 'energy'] * total_ref[year]

    switched_ref = fuel_ratio_ref.copy()[['fuels', 'year', 'new_energy']].rename(columns = {'new_energy': 'energy'})
    
    # Create metadata
    switched_ref['scenarios'] = 'reference'
    switched_ref['economy'] = economy
    switched_ref['sectors'] = '14_industry_sector'
    if sector in [ind1[0], ind1[1]]:
        switched_ref['sub1sectors'] = sector
        switched_ref['sub2sectors'] = 'x'
    else:
        switched_ref['sub1sectors'] = '14_03_manufacturing'
        switched_ref['sub2sectors'] = sector
    switched_ref['subfuels'] = 'x'

    # Organise the dataframe to be saved
    switched_ref = switched_ref[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels', 'year', 'energy']]

    # Define ne data frame copy for calcs that will overwrite current values
    switched_ref_calcs = switched_ref.copy()

    # Add in hydrogen for REF

    if (sector in ind2[:2]) & (hydrogen_ref):
        hyd_ref = hydrogen(fuel_mix = hyd_fuel_mix, start_year = hyd_start_ref, increment = hyd_increment_ref)
        for hyd_year in range(hyd_start_ref, proj_years[-1] + 1, 1):
            for fuel in switched_ref['fuels'].unique():
                relevant_year = switched_ref['year'] == hyd_year
                relevant_fuel = switched_ref['fuels'] == fuel   
                switched_ref.loc[(relevant_year) & (relevant_fuel), 'energy'] = switched_ref_calcs.loc[(relevant_year) & (relevant_fuel), 'energy'].values[0] *\
                    (1 - hyd_ref.loc[hyd_ref['year'] == hyd_year, 'share'].values[0])

            hyd_ref['energy'] = hyd_ref['fuel_ratio'] * hyd_ref['share'] * total_ref[hyd_year]

        hyd_ref['fuels'] = np.where(hyd_ref['fuel'] == '17_electricity', '17_electricity', '16_others')
        hyd_ref['subfuels'] = np.where(hyd_ref['fuels'] == '16_others', '16_x_hydrogen', 'x')

        # Metadata
        hyd_ref['scenarios'] = 'reference'
        hyd_ref['economy'] = economy
        hyd_ref['sectors'] = '14_industry_sector'
        hyd_ref['sub1sectors'] = '14_03_manufacturing'
        hyd_ref['sub2sectors'] = sector
        if sector == ind2[0]:
            hyd_ref['sub3sectors'] = '14_03_01_05_hydrogen'
        elif sector == ind2[1]:
            hyd_ref['sub3sectors'] = '14_03_02_01_fs'

        hyd_ref = hyd_ref[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels', 'subfuels', 'year', 'energy']]\
            .sort_values(['year', 'fuels']).reset_index(drop = True)
        
        hyd_ref.to_csv(hyd_ccs_location + economy + '_' + sector + '_hydrogen_ref.csv', index = False)

        # Now aggregate hydorgen results with steel
        switched_ref = switched_ref.merge(hyd_ref.drop(['sub3sectors'], axis = 1), how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        switched_ref['energy'] = switched_ref['energy_x'].fillna(0) + switched_ref['energy_y'].fillna(0)        
        switched_ref = switched_ref.drop(['energy_x', 'energy_y'], axis = 1)

        switched_ref = switched_ref.sort_values(['year', 'fuels']).copy().reset_index(drop = True)

    # Attach historical data
    if sector in [ind1[0], ind1[1]]:
        hist_ref = hist_data[(hist_data['economy'] == economy) &
                              (hist_data['sub1sectors'] == sector) &
                              (hist_data['sub2sectors'] == 'x') &
                              (hist_data['sub3sectors'] == 'x') &
                              (hist_data['sub4sectors'] == 'x') & 
                              (hist_data['fuels'].isin(data_ref['fuels'].unique())) &
                              (hist_data['subfuels'] == 'x')]
        
    else:
        hist_ref = hist_data[(hist_data['economy'] == economy) &
                              (hist_data['sub1sectors'] == '14_03_manufacturing') &
                              (hist_data['sub2sectors'] == sector) &
                              (hist_data['sub3sectors'] == 'x') &
                              (hist_data['sub4sectors'] == 'x') & 
                              (hist_data['fuels'].isin(data_ref['fuels'].unique())) &
                              (hist_data['subfuels'] == 'x')]
        
    hist_ref = hist_ref.melt(id_vars = hist_ref.columns[:9]).\
        rename(columns = {'variable': 'year',
                          'value': 'energy'}).\
                            drop(labels = ['sub3sectors', 'sub4sectors'], axis = 1)
    
    switched_ref = pd.concat([hist_ref, switched_ref]).copy().reset_index(drop = True)
    switched_ref['year'] = switched_ref['year'].astype(str).astype(int)

    switched_ref.to_csv(save_location + economy + '_' + sector + '_switched_ref.csv', index = False)

    # TGT
    total_tgt = data_tgt.copy().groupby('year').sum()['energy']
    
    for year in proj_years:    
        fuel_ratio_tgt.loc[fuel_ratio_tgt['year'] == year, 'new_energy'] = fuel_ratio_tgt.loc[fuel_ratio_tgt['year'] == year, 'energy'] * total_tgt[year]

    switched_tgt = fuel_ratio_tgt.copy()[['fuels', 'year', 'new_energy']].rename(columns = {'new_energy': 'energy'})
    
    # Create metadata
    switched_tgt['scenarios'] = 'target'
    switched_tgt['economy'] = economy
    switched_tgt['sectors'] = '14_industry_sector'
    if sector in [ind1[0], ind1[1]]:
        switched_tgt['sub1sectors'] = sector
        switched_tgt['sub2sectors'] = 'x'
    else:
        switched_tgt['sub1sectors'] = '14_03_manufacturing'
        switched_tgt['sub2sectors'] = sector
    switched_tgt['subfuels'] = 'x'

    # Organise the dataframe to be saved
    switched_tgt = switched_tgt[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels', 'year', 'energy']]

    # Define ne data frame copy for calcs that will overwrite current values
    switched_tgt_calcs = switched_tgt.copy()

    # Add in hydrogen for TGT

    if (sector in ind2[:2]) & (hydrogen_tgt):
        hyd_tgt = hydrogen(fuel_mix = hyd_fuel_mix, start_year = hyd_start_tgt, increment = hyd_increment_tgt)
        for hyd_year in range(hyd_start_tgt, proj_years[-1] + 1, 1):
            for fuel in switched_tgt['fuels'].unique():
                relevant_year = switched_tgt['year'] == hyd_year
                relevant_fuel = switched_tgt['fuels'] == fuel   
                switched_tgt.loc[(relevant_year) & (relevant_fuel), 'energy'] = switched_tgt_calcs.loc[(relevant_year) & (relevant_fuel), 'energy'].values[0] *\
                    (1 - hyd_tgt.loc[hyd_tgt['year'] == hyd_year, 'share'].values[0])

            hyd_tgt['energy'] = hyd_tgt['fuel_ratio'] * hyd_tgt['share'] * total_tgt[hyd_year]

        hyd_tgt['fuels'] = np.where(hyd_tgt['fuel'] == '17_electricity', '17_electricity', '16_others')
        hyd_tgt['subfuels'] = np.where(hyd_tgt['fuels'] == '16_others', '16_x_hydrogen', 'x')

        # Metadata
        hyd_tgt['scenarios'] = 'target'
        hyd_tgt['economy'] = economy
        hyd_tgt['sectors'] = '14_industry_sector'
        hyd_tgt['sub1sectors'] = '14_03_manufacturing'
        hyd_tgt['sub2sectors'] = sector
        if sector == ind2[0]:
            hyd_tgt['sub3sectors'] = '14_03_01_05_hydrogen'
        elif sector == ind2[1]:
            hyd_tgt['sub3sectors'] = '14_03_02_01_fs'

        hyd_tgt = hyd_tgt[['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'sub3sectors', 'fuels', 'subfuels', 'year', 'energy']]\
            .sort_values(['year', 'fuels']).reset_index(drop = True)
        
        hyd_tgt.to_csv(hyd_ccs_location + economy + '_' + sector + '_hydrogen_tgt.csv', index = False)

        # Now aggregate hydorgen results with steel
        switched_tgt = switched_tgt.merge(hyd_tgt.drop(['sub3sectors'], axis = 1), how = 'outer',
                                          on = ['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels', 'year']).reset_index(drop = True)
        
        switched_tgt['energy'] = switched_tgt['energy_x'].fillna(0) + switched_tgt['energy_y'].fillna(0)        
        switched_tgt = switched_tgt.drop(['energy_x', 'energy_y'], axis = 1)

        switched_tgt = switched_tgt.sort_values(['year', 'fuels']).copy().reset_index(drop = True)    


    # Attach historical data
    if sector in [ind1[0], ind1[1]]:
        hist_tgt = hist_data[(hist_data['economy'] == economy) &
                              (hist_data['sub1sectors'] == sector) &
                              (hist_data['sub2sectors'] == 'x') &
                              (hist_data['sub3sectors'] == 'x') &
                              (hist_data['sub4sectors'] == 'x') & 
                              (hist_data['fuels'].isin(data_tgt['fuels'].unique())) &
                              (hist_data['subfuels'] == 'x')]
        
    else:
        hist_tgt = hist_data[(hist_data['economy'] == economy) &
                              (hist_data['sub1sectors'] == '14_03_manufacturing') &
                              (hist_data['sub2sectors'] == sector) &
                              (hist_data['sub3sectors'] == 'x') &
                              (hist_data['sub4sectors'] == 'x') & 
                              (hist_data['fuels'].isin(data_tgt['fuels'].unique())) &
                              (hist_data['subfuels'] == 'x')]
        
    hist_tgt = hist_tgt.melt(id_vars = hist_tgt.columns[:9]).\
        rename(columns = {'variable': 'year',
                          'value': 'energy'}).\
                            drop(labels = ['sub3sectors', 'sub4sectors'], axis = 1)
    
    hist_tgt['scenarios'] = 'target'

    switched_tgt = pd.concat([hist_tgt, switched_tgt]).copy().reset_index(drop = True)
    switched_tgt['year'] = switched_tgt['year'].astype(str).astype(int)

    switched_tgt.to_csv(save_location + economy + '_' + sector + '_switched_tgt.csv', index = False)
    
    ##############################################################################################################################
    # Create some charts
    # Pivot the DataFrame
    chart_df_ref = switched_ref[(switched_ref['energy'] != 0) &
                                (switched_ref['year'] <= 2070)]
    
    # Custom chart column
    chart_df_ref['fuel'] = np.where(chart_df_ref['subfuels'] == 'x', chart_df_ref['fuels'], chart_df_ref['subfuels'])

    chart_pivot_ref = chart_df_ref.pivot(index = 'year', columns = 'fuel', values = 'energy')
    
    chart_df_tgt = switched_tgt[(switched_tgt['energy'] != 0) &
                                (switched_tgt['year'] <= 2070)]
    
    # Custom chart column
    chart_df_tgt['fuel'] = np.where(chart_df_tgt['subfuels'] == 'x', chart_df_tgt['fuels'], chart_df_tgt['subfuels'])

    chart_pivot_tgt = chart_df_tgt.pivot(index = 'year', columns = 'fuel', values = 'energy')

    # Define locations for chart index and custom labels
    max_y = 1.1 * max(chart_df_ref.groupby('year')['energy'].sum().max(), chart_df_tgt.groupby('year')['energy'].sum().max())
    proj_location = 0.925 * max_y

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))

    sns.set_theme(style = 'ticks')

    chart_pivot_ref.plot.area(ax = ax1,
                                stacked = True,
                                #alpha = 0.8,
                                color = fuel_palette1,
                                linewidth = 0)
    
    chart_pivot_tgt.plot.area(ax = ax2,
                                stacked = True,
                                #alpha = 0.8,
                                color = fuel_palette1,
                                linewidth = 0)
    
    if hydrogen_ref & ccs_ref:
        chart_title_ref = economy + ' ' + sector + ' REF\n' + 'Electrification rate: ' + str(elec_rate_ref) + \
            ', starting in ' + str(elec_start_ref) + '\nBiomass switch rate: ' + str(bio_rate_ref) + \
                ', starting in ' + str(bio_start_ref) + '\nCoal to gas switch rate: ' + str(c2g_rate_ref) + \
                    ', starting in ' + str(c2g_start_ref) + '\nHydrogen production begins ' + str(hyd_start_ref) + \
                    '\nCCS begins ' + str(ccs_start_ref)
    
    elif hydrogen_ref & (ccs_ref == False):
        chart_title_ref = economy + ' ' + sector + ' REF\n' + 'Electrification rate: ' + str(elec_rate_ref) + \
            ', starting in ' + str(elec_start_ref) + '\nBiomass switch rate: ' + str(bio_rate_ref) + \
                ', starting in ' + str(bio_start_ref) + '\nCoal to gas switch rate: ' + str(c2g_rate_ref) + \
                    ', starting in ' + str(c2g_start_ref) + '\nHydrogen production begins ' + str(hyd_start_ref)
        
    elif (hydrogen_ref == False) & ccs_ref:
        chart_title_ref = economy + ' ' + sector + ' REF\n' + 'Electrification rate: ' + str(elec_rate_ref) + \
            ', starting in ' + str(elec_start_ref) + '\nBiomass switch rate: ' + str(bio_rate_ref) + \
                ', starting in ' + str(bio_start_ref) + '\nCoal to gas switch rate: ' + str(c2g_rate_ref) + \
                    ', starting in ' + str(c2g_start_ref) + '\nCCS begins ' + str(ccs_start_ref)
        
    elif ((hydrogen_ref == False) & (ccs_ref == False)) | (sector not in [ind2[0], ind2[1], ind2[3]]):
        chart_title_ref = economy + ' ' + sector + ' REF\n' + 'Electrification rate: ' + str(elec_rate_ref) + \
            ', starting in ' + str(elec_start_ref) + '\nBiomass switch rate: ' + str(bio_rate_ref) + \
                ', starting in ' + str(bio_start_ref) + '\nCoal to gas switch rate: ' + str(c2g_rate_ref) + \
                    ', starting in ' + str(c2g_start_ref)

    ax1.set(title = chart_title_ref,
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            xlim = (2000, 2070),
            ylim = (0, max_y))
    
    if hydrogen_tgt & ccs_tgt:
        chart_title_tgt = economy + ' ' + sector + ' TGT\n' + 'Electrification rate: ' + str(elec_rate_tgt) + \
            ', starting in ' + str(elec_start_tgt) + '\nBiomass switch rate: ' + str(bio_rate_tgt) + \
                ', starting in ' + str(bio_start_tgt) + '\nCoal to gas switch rate: ' + str(c2g_rate_tgt) + \
                    ', starting in ' + str(c2g_start_tgt) + '\nHydrogen production begins ' + str(hyd_start_tgt) + \
                    '\nCCS begins ' + str(ccs_start_tgt)
    
    elif hydrogen_tgt & (ccs_tgt == False):
        chart_title_tgt = economy + ' ' + sector + ' TGT\n' + 'Electrification rate: ' + str(elec_rate_tgt) + \
            ', starting in ' + str(elec_start_tgt) + '\nBiomass switch rate: ' + str(bio_rate_tgt) + \
                ', starting in ' + str(bio_start_tgt) + '\nCoal to gas switch rate: ' + str(c2g_rate_tgt) + \
                    ', starting in ' + str(c2g_start_tgt) + '\nHydrogen production begins ' + str(hyd_start_tgt)
        
    elif (hydrogen_tgt == False) & ccs_tgt:
        chart_title_tgt = economy + ' ' + sector + ' TGT\n' + 'Electrification rate: ' + str(elec_rate_tgt) + \
            ', starting in ' + str(elec_start_tgt) + '\nBiomass switch rate: ' + str(bio_rate_tgt) + \
                ', starting in ' + str(bio_start_tgt) + '\nCoal to gas switch rate: ' + str(c2g_rate_tgt) + \
                    ', starting in ' + str(c2g_start_tgt) + '\nCCS begins ' + str(ccs_start_tgt)
        
    elif ((hydrogen_tgt == False) & (ccs_tgt == False)) | (sector not in [ind2[0], ind2[1], ind2[3]]):
        chart_title_tgt = economy + ' ' + sector + ' TGT\n' + 'Electrification rate: ' + str(elec_rate_tgt) + \
            ', starting in ' + str(elec_start_tgt) + '\nBiomass switch rate: ' + str(bio_rate_tgt) + \
                ', starting in ' + str(bio_start_tgt) + '\nCoal to gas switch rate: ' + str(c2g_rate_tgt) + \
                    ', starting in ' + str(c2g_start_tgt)

    ax2.set(title = chart_title_tgt,
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            xlim = (2000, 2070),
            ylim = (0, max_y))
    
    # Projection demarcation
    ax1.axvline(x = 2020, linewidth = 1, linestyle = '--', color = 'black')
    ax2.axvline(x = 2020, linewidth = 1, linestyle = '--', color = 'black')
    
    # Projection text
    ax1.annotate('Projection', 
                 xy = (2030, proj_location),
                 xytext = (2024, proj_location),
                 va = 'center',
                 ha = 'center',
                 fontsize = 9,
                 arrowprops = {'arrowstyle': '-|>',
                               'lw': 0.5,
                               'ls': '-',
                               'color': 'black'})
    
    ax2.annotate('Projection', 
                 xy = (2030, proj_location),
                 xytext = (2024, proj_location),
                 va = 'center',
                 ha = 'center',
                 fontsize = 9,
                 arrowprops = {'arrowstyle': '-|>',
                               'lw': 0.5,
                               'ls': '-',
                               'color': 'black'})
    
    ax1.legend(title = '', fontsize = 8)
    ax2.legend(title = '', fontsize = 8)
            
    plt.tight_layout()
    plt.savefig(save_location + economy + '_' + sector + '_elec.png')
    plt.show()
    plt.close()


# Iron and steel
fuel_switch(economy = '19_THA', sector = ind2[0], hydrogen_ref = True, hydrogen_tgt = True)