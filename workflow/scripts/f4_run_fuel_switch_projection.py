# Run the fuel switch model for economies import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Import function
from f2_fuel_switch_function import fuel_switch, hydrogen
from f3_non_energy_switch_function import fuel_switch_ne

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]

# Modelled years
proj_years = list(range(2021, 2101, 1))

# Historical energy data
hist_egeda = pd.read_csv(latest_EGEDA).loc[:, :'2020']

# Vectors for switching
# don't electrify
no_elec = ['12_solar', '17_electricity', '18_heat']
# biomass doesnt switch for the below fuels 
no_biomass = ['12_solar', '15_solid_biomass', '17_electricity', '18_heat']
# To gas (from coal); aka these fuels dont get switched from:
to_gas = ['06_crude_oil_and_ngl', '07_petroleum_products', '08_gas', '12_solar', '15_solid_biomass',
          '16_others', '17_electricity', '18_heat']

# CCS fuels
ccs_fuels = ['01_coal', '02_coal_products', '08_gas']

# Run the function for the different economies
##################################################################################################################
# Japan
# Mining
fuel_switch(economy = '08_JPN', sector = ind1[0])

# Construction
fuel_switch(economy = '08_JPN', sector = ind1[1])

# Iron and steel
fuel_switch(economy = '08_JPN', sector = ind2[0], elec_rate_ref = 0.001, elec_rate_tgt = 0.005, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, hyd_start_tgt = 2025, ccs_tgt = True)

# Chemicals
fuel_switch(economy = '08_JPN', sector = ind2[1], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005,
            hydrogen_ref = False, hydrogen_tgt = False, ccs_ref = False, ccs_tgt = True)

# Non-ferrous metals
fuel_switch(economy = '08_JPN', sector = ind2[2])

# Non-metallic minerals
fuel_switch(economy = '08_JPN', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            bio_rate_tgt = 0.001, ccs_tgt = True)

# Transport
fuel_switch(economy = '08_JPN', sector = ind2[4])

# Machinery
fuel_switch(economy = '08_JPN', sector = ind2[5])

# Food and Beverages
fuel_switch(economy = '08_JPN', sector = ind2[6], elec_rate_tgt = 0.0075)

# Pulp and paper
fuel_switch(economy = '08_JPN', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_tgt = 0.01)

# Wood
fuel_switch(economy = '08_JPN', sector = ind2[8])

# Textiles
fuel_switch(economy = '08_JPN', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.01)

# Non-specified
fuel_switch(economy = '08_JPN', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy
fuel_switch_ne(economy = '08_JPN', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005)

#################################################################################################################
# Thailand
# Mining
fuel_switch(economy = '19_THA', sector = ind1[0])

# Construction
fuel_switch(economy = '19_THA', sector = ind1[1])

# Iron and steel
fuel_switch(economy = '19_THA', sector = ind2[0], elec_rate_ref = 0.001, elec_rate_tgt = 0.0025, 
            hydrogen_ref = True, ccs_ref = False, hydrogen_tgt = True, ccs_tgt = True)

# Chemicals
fuel_switch(economy = '19_THA', sector = ind2[1], elec_rate_ref = 0.0025, elec_rate_tgt = 0.005,
            hydrogen_ref = False, hydrogen_tgt = False, ccs_ref = False, ccs_tgt = True)

# Non-ferrous metals
fuel_switch(economy = '19_THA', sector = ind2[2])

# Non-metallic minerals
fuel_switch(economy = '19_THA', sector = ind2[3], elec_rate_ref = 0.0015, elec_rate_tgt = 0.003, 
            bio_rate_tgt = 0.001, ccs_tgt = True)

# Transport
fuel_switch(economy = '19_THA', sector = ind2[4])

# Machinery
fuel_switch(economy = '19_THA', sector = ind2[5])

# Food and Beverages
fuel_switch(economy = '19_THA', sector = ind2[6], elec_rate_tgt = 0.0075)

# Pulp and paper
fuel_switch(economy = '19_THA', sector = ind2[7], elec_rate_ref = 0.0025, elec_rate_tgt = 0.008, 
            bio_rate_tgt = 0.006)

# Wood
fuel_switch(economy = '19_THA', sector = ind2[8])

# Textiles
fuel_switch(economy = '19_THA', sector = ind2[9], elec_rate_ref = 0.003, elec_rate_tgt = 0.006, 
            bio_rate_tgt = 0.002)

# Non-specified
fuel_switch(economy = '19_THA', sector = ind2[10], elec_rate_tgt = 0.01)

# Non-energy
fuel_switch_ne(economy = '19_THA', hyd_increment_ref = 0.002, hyd_increment_tgt = 0.005)

#################################################################################################

# Now read in all data for each economy
for economy in [list(economy_select)[-3]]:
    data_location = './results/industry/3_fuel_switch/{}/'.format(economy)

    if not os.path.isdir(data_location):
        os.makedirs(data_location)

    all_sector_save = './results/industry/3_fuel_switch/{}/all_sectors/'.format(economy)

    if not os.path.isdir(all_sector_save):
        os.makedirs(all_sector_save)

    economy_df = pd.DataFrame()

    economy_files = glob.glob(data_location + '*.csv')

    for i in economy_files:
        temp_df = pd.read_csv(i)
        economy_df = pd.concat([economy_df, temp_df]).copy().reset_index(drop = True)

    economy_df.to_csv(all_sector_save + '{}_all_subsectors.csv'.format(economy), index = False)
    
    # Create some charts
    # Pivot the DataFrame
    chart_df_ref = economy_df[(economy_df['energy'] != 0) &
                              (economy_df['energy'].isna() == False) &
                              (economy_df['scenarios'] == 'reference') &
                              (economy_df['year'] <= 2070)].copy().reset_index(drop = True)
    
    # Custom chart column
    chart_df_ref['fuel'] = np.where(chart_df_ref['subfuels'] == 'x', chart_df_ref['fuels'], chart_df_ref['subfuels'])
    
    chart_df_ref = chart_df_ref.groupby(['fuel', 'year'])['energy'].sum().reset_index()
    
    chart_pivot_ref = chart_df_ref.pivot(index = 'year', columns = 'fuel', values = 'energy')
    
    chart_df_tgt = economy_df[(economy_df['energy'] != 0) &
                              (economy_df['energy'].isna() == False) & 
                              (economy_df['scenarios'] == 'target') &
                              (economy_df['year'] <= 2070)].copy().reset_index(drop = True)
    
    # Custom chart column
    chart_df_tgt['fuel'] = np.where(chart_df_tgt['subfuels'] == 'x', chart_df_tgt['fuels'], chart_df_tgt['subfuels'])
    
    chart_df_tgt = chart_df_tgt.groupby(['fuel', 'year'])['energy'].sum().reset_index()

    chart_pivot_tgt = chart_df_tgt.pivot(index = 'year', columns = 'fuel', values = 'energy')

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
    
    ax1.set(title = economy + ' all industry REF',
            xlabel = 'Year',
            ylabel = 'Energy (PJ)',
            xlim = (2000, 2070),
            ylim = (0, max_y))
    
    ax2.set(title = economy + ' all industry TGT',
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
    
    ax1.legend(title = '', fontsize = 7)
    ax2.legend(title = '', fontsize = 7)

    #ax2.set_ylim(ax1.get_ylim())
            
    plt.tight_layout()
    plt.savefig(all_sector_save + economy + '_industry.png')
    plt.show()
    plt.close()