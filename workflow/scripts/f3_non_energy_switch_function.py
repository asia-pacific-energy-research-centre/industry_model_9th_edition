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
    
    ## REF ###########################################################################################
    # Build in hydrogen switch
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
    
    # Bring in historical
    hist_ref = hist_data[(hist_data['economy'] == economy) &
                         (hist_data['sectors'] == '17_nonenergy_use') &
                         (hist_data['sub1sectors'] == 'x') &
                         (hist_data['sub2sectors'] == 'x') &
                         (hist_data['sub3sectors'] == 'x') &
                         (hist_data['sub4sectors'] == 'x') & 
                         (hist_data['fuels'].isin(data_ref['fuels'].unique())) &
                         (hist_data['subfuels'] == 'x')]
    
    hist_ref = hist_ref.melt(id_vars = hist_ref.columns[:9]).\
        rename(columns = {'variable': 'year',
                          'value': 'energy'}).\
                            drop(labels = ['sub2sectors', 'sub3sectors', 'sub4sectors'], axis = 1)
    
    switched_ref = pd.concat([hist_ref, switched_ref]).copy().reset_index(drop = True)
    switched_ref['year'] = switched_ref['year'].astype(str).astype(int)

    final_ref = pd.DataFrame()

    for year in switched_ref['year'].unique():
        temp_df = switched_ref[switched_ref['year'] == year].copy()
        new_line = switched_ref[(switched_ref['year'] == year) &
                                (switched_ref['fuels'] == '16_others')].copy().reset_index(drop = True)
        
        new_line.loc[0, 'subfuels'] = '16_x_hydrogen'
        temp_df = pd.concat([temp_df, new_line]).sort_values('fuels').copy().reset_index(drop = True)

        final_ref = pd.concat([final_ref, temp_df]).copy().reset_index(drop = True)

    final_ref.to_csv(save_location + economy + '_non_energy_switched_ref.csv', index = False)

    ## TGT ###########################################################################################
    # Build in hydrogen switch
    for year in proj_years[1:]:
        if hyd_start_tgt > year:
            ratio_nextyear = ne_ratio_tgt[ne_ratio_tgt['year'] == year - 1].copy()
            ratio_nextyear['year'] = year
            ne_ratio_tgt = pd.concat([ne_ratio_tgt, ratio_nextyear]).copy().reset_index(drop = True)

        else:    
            ratio_nextyear = ne_ratio_tgt[ne_ratio_tgt['year'] == year - 1].copy()
            ratio_thisyear = ratio_nextyear.copy()
            ratio_nextyear['year'] = year

            non_zero_tgt = list(ratio_nextyear[(ratio_nextyear['energy'] != 0) &
                                               (ratio_nextyear['year'] == year)]['fuels'])
            non_zero_ne_tgt = [i for i in non_zero_tgt]
    
            for fuel in non_zero_ne_tgt:
                if (hyd_increment_tgt / (len(non_zero_ne_tgt)) >= ratio_thisyear.loc[ratio_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    ratio_nextyear.loc[ratio_nextyear['fuels'] == fuel, 'energy'] = 0

                elif (hyd_increment_tgt / (len(non_zero_ne_tgt)) < ratio_thisyear.loc[ratio_thisyear['fuels'] == fuel, 'energy'].values[0]):
                    # New value for fuel
                    ratio_nextyear.loc[ratio_nextyear['fuels'] == fuel, 'energy'] = ratio_thisyear.loc[ratio_thisyear['fuels'] == fuel, 'energy'].values[0] - \
                        (hyd_increment_tgt / (len(non_zero_ne_tgt)))
                
            # New value for electricity
            if (1 - ratio_thisyear.loc[ratio_thisyear['fuels'] == '16_others', 'energy'].values[0]) < hyd_increment_tgt:
                ratio_nextyear.loc[ratio_nextyear['fuels'] == '16_others', 'energy'] = 1.0 

            elif (1 - ratio_thisyear.loc[ratio_thisyear['fuels'] == '16_others', 'energy'].values[0]) >= hyd_increment_tgt:
                ratio_nextyear.loc[ratio_nextyear['fuels'] == '16_others', 'energy'] = ratio_thisyear.loc[ratio_thisyear['fuels'] == '16_others', 'energy'].values[0] + hyd_increment_tgt

            ne_ratio_tgt = pd.concat([ne_ratio_tgt, ratio_nextyear]).copy().reset_index(drop = True)

    # Ensure that the sum of the ratio remains 1 for all years 
    grouped_tgt = ne_ratio_tgt.groupby('year')

    for year, group in grouped_tgt:
        sum_energy = group['energy'].sum()

        if sum_energy != 1:
            group['energy'] = group['energy'] / sum_energy

        ne_ratio_tgt.loc[group.index] = group

    # Now use the updated fuel share dataframe to deliver new energy results, that have been electrified
    # Grab total energy by year
    # TGT
    total_tgt = data_tgt.copy().groupby('year').sum()['energy']
    
    for year in proj_years:    
        ne_ratio_tgt.loc[ne_ratio_tgt['year'] == year, 'new_energy'] = ne_ratio_tgt.loc[ne_ratio_tgt['year'] == year, 'energy'] * total_tgt[year]

    switched_tgt = ne_ratio_tgt.copy()[['fuels', 'year', 'new_energy']].rename(columns = {'new_energy': 'energy'})
    
    # Create metadata
    switched_tgt['scenarios'] = 'target'
    switched_tgt['economy'] = economy
    switched_tgt['sectors'] = '17_nonenergy_use'
    switched_tgt['sub1sectors'] = 'x'
    switched_tgt['subfuels'] = 'x'

    # Organise the dataframe to be saved
    switched_tgt = switched_tgt[['scenarios', 'economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels', 'year', 'energy']]
    
    # Bring in historical
    # Already exists from REF
    hist_tgt = hist_ref.copy()
    hist_tgt['scenarios'] = 'target'
     
    switched_tgt = pd.concat([hist_tgt, switched_tgt]).copy().reset_index(drop = True)
    switched_tgt['year'] = switched_tgt['year'].astype(str).astype(int)

    final_tgt = pd.DataFrame()

    for year in switched_tgt['year'].unique():
        temp_df = switched_tgt[switched_tgt['year'] == year].copy()
        new_line = switched_tgt[(switched_tgt['year'] == year) &
                                (switched_tgt['fuels'] == '16_others')].copy().reset_index(drop = True)
        
        new_line.loc[0, 'subfuels'] = '16_x_hydrogen'
        temp_df = pd.concat([temp_df, new_line]).sort_values('fuels').copy().reset_index(drop = True)

        final_tgt = pd.concat([final_tgt, temp_df]).copy().reset_index(drop = True)

    final_tgt.to_csv(save_location + economy + '_non_energy_switched_tgt.csv', index = False)

    ##############################################################################################################################
    # Create some charts
    # Pivot the DataFrame
    # REF
    chart_df_ref = switched_ref[(switched_ref['energy'] != 0) &
                                (switched_ref['year'] <= 2070)]
    
    # Custom chart column
    chart_df_ref['fuel'] = np.where(chart_df_ref['fuels'] == '16_others', '16_x_hydrogen', chart_df_ref['fuels'])

    chart_pivot_ref = chart_df_ref.pivot(index = 'year', columns = 'fuel', values = 'energy')

    # TGT
    chart_df_tgt = switched_tgt[(switched_tgt['energy'] != 0) &
                                (switched_tgt['year'] <= 2070)]
    
    # Custom chart column
    chart_df_tgt['fuel'] = np.where(chart_df_tgt['fuels'] == '16_others', '16_x_hydrogen', chart_df_tgt['fuels'])

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
    
    chart_title_ref = economy + ' non-energy use REF\n' + 'Hydrogen rate: ' + str(hyd_increment_ref) + \
        ', starting in ' + str(hyd_start_ref)
    
    chart_title_tgt = economy + ' non-energy use TGT\n' + 'Hydrogen rate: ' + str(hyd_increment_tgt) + \
        ', starting in ' + str(hyd_start_tgt)

    ax1.set(title = chart_title_ref,
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            xlim = (2000, 2070),
            ylim = (0, max_y))

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
    plt.savefig(save_location + economy + '_non_energy.png')
    plt.show()
    plt.close()

