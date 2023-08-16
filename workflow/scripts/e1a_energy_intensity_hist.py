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

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()

# Read in historical production data
hist_prod = pd.read_csv('./data/industry_production/3_industry_projections/interim_all_sectors.csv')
hist_prod = hist_prod[hist_prod['year'] <= 2020]

# Sectors that we have production data for 
relevant_sectors = hist_prod['sub2sectors'].unique()[[1, 2, 3, 4, 5, 6, 7, 10]]

# Read in energy data
EGEDA_2020 = pd.read_csv(latest_EGEDA)

EGEDA_2020 = EGEDA_2020[(EGEDA_2020['sub1sectors'].str.startswith('14_')) &
                        (EGEDA_2020['fuels'] == '19_total') &
                        (EGEDA_2020['sub3sectors'] == 'x')]\
                            .copy().reset_index(drop = True).loc[:, :'2020']

EGEDA_2020 = EGEDA_2020.melt(id_vars = ['economy', 'sub1sectors', 'sub2sectors'],
                             value_vars = [str(i) for i in list(range(1980, 2021, 1))],
                             var_name = 'year',
                             value_name = 'energy')

EGEDA_2020['year'] = EGEDA_2020['year'].astype('int')

# Energy intensity analysis
for economy in hist_prod['economy_code'].unique():
    # Define empty datadrame to save all en_int for each economy
    en_int_economy_df = pd.DataFrame()
    for sector in relevant_sectors:
        energy_df = EGEDA_2020[(EGEDA_2020['economy'] == economy) &
                               (EGEDA_2020['sub2sectors'] == sector)].copy().reset_index(drop = True)
        
        prod_df = hist_prod[(hist_prod['economy_code'] == economy) &
                            (hist_prod['sub2sectors'] == sector)].copy().reset_index(drop = True)

        energy_intensity = energy_df.merge(prod_df[['year', 'value']], on = 'year')

        energy_intensity['en_intensity'] = energy_intensity['energy'] / energy_intensity['value']
        energy_intensity['percent'] = energy_intensity[['en_intensity']].apply(pd.Series.pct_change)

        en_int_economy_df = pd.concat([en_int_economy_df, energy_intensity]).copy().reset_index(drop = True)

        save_location = './data/energy_intensity/{}/'.format(economy)

        if not os.path.isdir(save_location):
            os.makedirs(save_location)
        
        if energy_intensity.empty:
            pass

        else:
            # Charts
            fig, ax1 = plt.subplots()

            chart_df = energy_intensity.groupby(['year']).agg({'percent': 'sum', 'en_intensity': 'sum'})
            chart_df = chart_df.reset_index()
            chart_df['xaxis'] = range(len(chart_df))

            sns.set_theme(style = 'ticks')

            sns.barplot(data = chart_df,
                        x = 'xaxis',
                        y = 'percent',
                        color = 'orange',
                        ax = ax1)
            
            ax2 = ax1.twinx()

            sns.lineplot(data = chart_df,
                         x = 'xaxis',
                         y = 'en_intensity',
                         ax = ax2)                        

            ax1.set(title = economy + ' ' + sector + ' energy intensity',
                    xlabel = 'Year',
                    ylabel = 'Energy intensity percent change',
                    xticks = chart_df.index[range(0, chart_df.index.max() + 1, 5)],
                    xticklabels = chart_df['year'][range(0, chart_df.index.max() + 1, 5)])
            
            ax2.set(ylabel = 'Energy intensity series',
                    ylim = (0, chart_df['en_intensity'].max() * 1.1))
            
            #ax1.set_xticklabels(chart_df['year'].values)
                    
            plt.tight_layout()
            plt.savefig(save_location + economy + '_' + sector + '.png')
            plt.show()
            plt.close()

        en_int_economy_df.to_csv(save_location + economy + '_en_intensity.csv', index = False)