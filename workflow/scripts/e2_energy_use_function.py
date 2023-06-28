# Overlaying energy intensity improvements onto production estimates
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())



# Grab insudtrial production trajectories
indprod_df = pd.read_csv(latest_prod)

def energy_use(economy = '01_AUS',
               sub1sectors = '14_01_mining_and_quarrying', 
               sub2sectors = 'x',
               increment_ref = 0.01,
               increment_tgt = 0.02,
               start_year = 2022,
               end_year = 2050,
               data = indprod_df):
    
    # Where to save files
    industry_energy = './results/industry/1_total_energy_subsector/{}/'.format(economy)

    if not os.path.isdir(industry_energy):
        os.makedirs(industry_energy)

    # Relevant dataframe grab
    sector_prod_df = data[(data['economy_code'] == economy) &
                          (data['sub1sectors'] == sub1sectors) &
                          (data['sub2sectors'] == sub2sectors)].copy().reset_index(drop = True)
    
    # New column with total energy trajectory
    sector_prod_df['energy'] = np.nan
    sector_prod_df = sector_prod_df.set_index('year')

    # Reference data frame
    ref_df = sector_prod_df[sector_prod_df['scenario'] == 'reference'].copy()
    
    # Target data frame
    tgt_df = sector_prod_df[sector_prod_df['scenario'] == 'target'].copy()

    ref_dict = {}
    for year in ref_df.index:
        if (year >= start_year) & (year <= end_year):
            ref_dict[year] = (1 - increment_ref) * ref_dict[year - 1]

        elif year > end_year:
            ref_dict[year] = ref_dict[year - 1]

        elif year < start_year:
            ref_dict[year] = 1

    tgt_dict = {}
    for year in tgt_df.index:
        if (year >= start_year) & (year <= end_year):
            tgt_dict[year] = (1 - increment_tgt) * tgt_dict[year - 1]

        elif (year > end_year):
            tgt_dict[year] = tgt_dict[year - 1]

        elif year < start_year:
            tgt_dict[year] = 1

    for year in ref_df.index:
        ref_df.loc[year, 'energy'] = ref_df.loc[year, 'value'] * ref_dict[year]
        tgt_df.loc[year, 'energy'] = tgt_df.loc[year, 'value'] * tgt_dict[year]
    

    both_sectors = pd.concat([ref_df, tgt_df]).copy().reset_index()

    # Now chart the result
    chart_df = both_sectors[(both_sectors['year'] <= 2070) &
                            (both_sectors['year'] >= 2017)].copy()

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                x = 'year',
                y = 'energy',
                hue = 'scenario')

    ax.set(title = economy + ' ' + sub1sectors + ' ' + sub2sectors,
           xlabel = 'Year',
           ylabel = 'Total energy use index (2017 = 100)',
           ylim = (0, chart_df['energy'].max() * 1.1))

    plt.legend(title = '')

    plt.tight_layout()
    plt.show()

    if sub2sectors == 'x':
        fig.savefig(industry_energy + economy + '_' + sub1sectors + '.png')
    elif sub1sectors == '14_03_manufacturing':
        fig.savefig(industry_energy + economy + '_' + sub2sectors + '.png')
    else:
        pass
    
    plt.close()
    
    if sub2sectors == 'x':
        both_sectors.to_csv(industry_energy + economy + '_' + sub1sectors + '.csv', index = False)
    elif sub1sectors == '14_03_manufacturing':
        both_sectors.to_csv(industry_energy + economy + '_' + sub2sectors + '.csv', index = False)
    else:
        pass

energy_use(increment_ref = 0.01, increment_tgt = 0.015, end_year = 2030)