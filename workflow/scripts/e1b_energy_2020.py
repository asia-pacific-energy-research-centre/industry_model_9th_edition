# Interim projections
# Set working directory to be the project folder
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Read in historical industry energy data
EGEDA_df = pd.read_csv(latest_EGEDA)

EGEDA_ind_df = EGEDA_df[(EGEDA_df['sub1sectors'].str.startswith('14_')) &
                        (EGEDA_df['sub3sectors'] == 'x')]\
                            .copy().reset_index(drop = True).loc[:, :'2020']

EGEDA_ind_df = EGEDA_ind_df.melt(id_vars = ['economy', 'sub1sectors', 'sub2sectors', 'fuels'],
                             value_vars = [str(i) for i in list(range(1980, 2021, 1))],
                             var_name = 'year',
                             value_name = 'energy')

EGEDA_ind_df['year'] = EGEDA_ind_df['year'].astype('int')

EGEDA_ind_df['sector'] = EGEDA_ind_df['sub1sectors'].where(EGEDA_ind_df['sub2sectors'] == 'x', 
                                                                 EGEDA_ind_df['sub2sectors'])

# Subset the data so there is only EGEDA industry total energy use
EGEDA_ind_total = EGEDA_ind_df[EGEDA_ind_df['fuels'] == '19_total'].copy().reset_index(drop = True)

economy_list = list(EGEDA_ind_df['economy'].unique())[:-7]

# Energy by subsector in 2020
for economy in economy_list:
    energy_df = EGEDA_ind_total[(EGEDA_ind_total['economy'] == economy) &
                                (EGEDA_ind_total['energy'] != 0) & 
                                (EGEDA_ind_total['sector'] != '14_03_manufacturing') & 
                                (EGEDA_ind_total['year'].isin([2019, 2020]))].copy().reset_index(drop = True)
    
    energy_df['cumulative'] = energy_df.groupby(['year', 'sector'])['energy'].cumsum()

    save_location = './data/EGEDA/energy_charts/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    # Pivot the DataFrame
    stacked_df = energy_df.pivot(index = 'year', columns = 'sector', values = 'cumulative')

    # Chart
    fig, ax = plt.subplots(figsize = (5, 7))

    sns.set_theme(style = 'ticks')

    stacked_df.plot(kind = 'bar', stacked = True, ax = ax)

    max_y = max(energy_df[energy_df['year'] == 2019]['energy'].sum(), 
                energy_df[energy_df['year'] == 2020]['energy'].sum())

    ax.set(title = economy + ' industry energy use 2020',
           xlabel = 'Year',
           ylabel = 'Petajoules',
           ylim = (0, max_y * 1.1))

    plt.legend(title = '', fontsize = 8)

    plt.tight_layout()
    plt.show()
    fig.savefig(save_location + economy + '_industry_energy_2020.png')


# Subsector energy mix
# Now subset so there is only use of relevant fuels
relevant1 = fuels_list[[0, 1, 5, 6, 7, 14, 15, 16, 17]]
relevant2 = subfuels_list[[27, 28, 29, 30, 31, 32, 34, 35, 36, 37]]

EGEDA_ind_df = EGEDA_df[(EGEDA_df['sub1sectors'].str.startswith('14_')) &
                        (EGEDA_df['sub3sectors'] == 'x') & 
                        (EGEDA_df['fuels'].isin(relevant1)) &
                        (EGEDA_df['subfuels'] == 'x')]\
                            .copy().reset_index(drop = True).loc[:, :'2020']

EGEDA_ind_df['sector'] = EGEDA_ind_df['sub1sectors'].where(EGEDA_ind_df['sub2sectors'] == 'x', 
                                                                 EGEDA_ind_df['sub2sectors'])

EGEDA_ind_df = EGEDA_ind_df.melt(id_vars = ['economy', 'sector', 'fuels'],
                                 value_vars = [str(i) for i in list(range(1980, 2021, 1))],
                                 var_name = 'year',
                                 value_name = 'energy')

EGEDA_ind_df['year'] = EGEDA_ind_df['year'].astype('int')

# Energy by subsector in 2020
for economy in economy_list:
    # Save location for charts
    save_location = './data/EGEDA/energy_charts/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)
    
    for sector in EGEDA_ind_df['sector'].unique():
        energy_df = EGEDA_ind_df[(EGEDA_ind_df['economy'] == economy) &
                                 (EGEDA_ind_df['energy'] != 0) & 
                                 (EGEDA_ind_df['sector'] == sector) & 
                                 (EGEDA_ind_df['year'].isin([2019, 2020]))].copy().reset_index(drop = True)
        
        if energy_df.empty:
            pass
        
        else:
            energy_df['cumulative'] = energy_df.groupby(['year', 'fuels'])['energy'].cumsum()  

            # Pivot the DataFrame
            stacked_df = energy_df.pivot(index = 'year', columns = 'fuels', values = 'cumulative')

            # Chart
            fig, ax = plt.subplots(figsize = (5, 7))

            sns.set_theme(style = 'ticks')

            stacked_df.plot(kind = 'bar', stacked = True, ax = ax, color = fuel_palette4)

            max_y = max(energy_df[energy_df['year'] == 2019]['energy'].sum(),
                        energy_df[energy_df['year'] == 2020]['energy'].sum())

            ax.set(title = economy + ' ' + sector + ' fuel',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (0, max_y * 1.1))

            plt.legend(title = '', fontsize = 8)

            plt.tight_layout()
            plt.show()
            fig.savefig(save_location + economy + '_' + sector + '.png')