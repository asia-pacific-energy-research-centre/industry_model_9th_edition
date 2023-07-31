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

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Modelled years
proj_years = list(range(2021, 2101, 1))

# Also grab historical energy data
hist_egeda = pd.read_csv(latest_EGEDA).loc[:, :'2020']

# Master function for all fuel switching
for economy in economy_select[-3:-2]:

    save_location = './results/non_energy/3_finalisation/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    # Grab the relevant data to manipulate the fuel shares
    data_ref = pd.read_csv('./results/non_energy/2_nonenergy_projections/{}/{}_non_energy_ref.csv'.format(economy, economy))
    data_tgt = pd.read_csv('./results/non_energy/2_nonenergy_projections/{}/{}_non_energy_tgt.csv'.format(economy, economy))

    data_ref['scenarios'] = 'reference'
    data_tgt['scenarios'] = 'target'

    data_ref = data_ref[['scenarios', 'economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels', 'year', 'energy']].copy()
    data_tgt = data_tgt[['scenarios', 'economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels', 'year', 'energy']].copy()

    # Historical
    hist_ref = hist_egeda[(hist_egeda['economy'] == economy) &
                              (hist_egeda['sectors'] == '17_nonenergy_use') &
                              (hist_egeda['sub1sectors'] == 'x') &
                              (hist_egeda['sub2sectors'] == 'x') &
                              (hist_egeda['sub3sectors'] == 'x') &
                              (hist_egeda['sub4sectors'] == 'x') & 
                              (hist_egeda['fuels'].isin(data_ref['fuels'].unique())) &
                              (hist_egeda['subfuels'] == 'x')]
        
    hist_ref = hist_ref.melt(id_vars = hist_ref.columns[:9]).\
        rename(columns = {'variable': 'year',
                          'value': 'energy'}).\
                            drop(labels = ['sub2sectors', 'sub3sectors', 'sub4sectors'], axis = 1)
    
    hist_tgt = hist_ref.copy()
    hist_tgt['scenarios'] = 'target'
    
    # Combine REF
    combined_ref = pd.concat([hist_ref, data_ref]).copy().reset_index(drop = True)
    combined_ref['year'] = combined_ref['year'].astype(str).astype(int)

    combined_ref.to_csv(save_location + economy + '_non_energy_ref.csv', index = False)

    # Combine TGT
    combined_tgt = pd.concat([hist_tgt, data_tgt]).copy().reset_index(drop = True)
    combined_tgt['year'] = combined_tgt['year'].astype(str).astype(int)

    combined_tgt.to_csv(save_location + economy + '_non_energy_tgt.csv', index = False)
 
    ##############################################################################################################################
    # Create some charts
    # Pivot the DataFrame
    chart_df_ref = combined_ref[(combined_ref['energy'] != 0) &
                                (combined_ref['year'] <= 2070)]

    chart_pivot_ref = chart_df_ref.pivot(index = 'year', columns = 'fuels', values = 'energy')
    
    chart_df_tgt = combined_tgt[(combined_tgt['energy'] != 0) &
                                (combined_tgt['year'] <= 2070)]

    chart_pivot_tgt = chart_df_tgt.pivot(index = 'year', columns = 'fuels', values = 'energy')

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

    ax1.set(title = economy + ' non-energy',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            xlim = (2000, 2070),
            ylim = (0, max_y))

    ax2.set(title = economy + ' non-energy',
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