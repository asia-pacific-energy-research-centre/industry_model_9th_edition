# Combining data to get trajectories for industrial sector as defined in EGEDA EBT
import os
import re 

wanted_wd = 'industry_model_9th_edition'

os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Read in gdp data
APEC_gdp = pd.read_csv('./data/macro/APEC_GDP_population.csv')
APEC_gdp = APEC_gdp[APEC_gdp['variable'] == 'real_GDP'].copy().reset_index(drop = True)

# Read in WDI industry share of GDP (or manufacturing) data
APEC_indshare = pd.read_csv('./data/industry_interim/wdi_projections.csv')
APEC_indshare.series_code.unique()[2:]

#############################################################################################
# Chemicals, M & T, F & B, Textiles, and Other subsector example
for economy in APEC_gdp['economy_code'].unique():
    for sector in APEC_indshare['series_code'].unique()[2:]:
        gdp_data = APEC_gdp[APEC_gdp['economy_code'] == economy].copy().reset_index(drop = True)
        
        manu_share = APEC_indshare[(APEC_indshare['economy_code'] == economy) &
                                (APEC_indshare['series_code'] == 'NV.IND.MANF.ZS')].copy().reset_index(drop = True)
        
        sub_share = APEC_indshare[(APEC_indshare['economy_code'] == economy) &
                                (APEC_indshare['series_code'] == sector)].copy().reset_index(drop = True)
        
        # Now create new series, first join the date to get GDP, manufacturing and chem share of manufacturing
        combined_data = gdp_data.merge(manu_share, left_on = 'year', right_on = 'year')\
            .merge(sub_share, left_on = 'year', right_on = 'year').dropna().reset_index(drop = True)
        
        if combined_data.empty:
            pass

        else:
            # Generate chemical production by multiplying GDP, manufacturing share of GDP, and subsector 
            # share of manufacturing
            combined_data['sub_production'] = (combined_data['value_x'] * \
                (combined_data['value_y'] / 100) * (combined_data['value'] / 100))
            
            # Make 2018 the base year
            base_year = combined_data.loc[combined_data['year'] == 2018, 'sub_production']\
                .reset_index(drop = True).values[0]
            
            combined_data['indexed'] = combined_data['sub_production'] / base_year * 100
            
            # Generate dataframe with production index for earliest year possible out to 2100
            combined_data = combined_data[['economy_code_x', 'economy_x', 'year', 'indexed']].copy()\
                .rename(columns = {'economy_code_x': 'economy_code',
                                   'economy_x': 'economy',
                                   'indexed': 'value'})
            
            combined_data['series'] = sector + ' index (2018 = 100)'

            combined_data = combined_data[['economy', 'economy_code', 'series', 'year', 'value']].copy()
            
            # Save data
            save_data = './data/industry_production/{}/'.format(economy)

            if not os.path.isdir(save_data):
                os.makedirs(save_data)

            combined_data.to_csv(save_data + economy + '_' + sector + '.csv', index = False) 

            # Construct some plots
            fig, ax = plt.subplots()

            sns.set_theme(style = 'ticks')

            sns.lineplot(data = combined_data, 
                            x = 'year',
                            y = 'value',
                            hue = 'series')
            
            ax.set(title = economy,
                xlabel = 'year',
                ylabel = sector,
                ylim = (0, combined_data['value'].max() * 1.1),
                xlim = (combined_data['year'].min(), 2070))
            
            plt.legend(title = '')
            
            plt.tight_layout()
            plt.savefig(save_data + economy + '_' + sector + '.png')
            plt.show()
            plt.close()

# Now package up all the results and save in one combined data frame
combined_df = pd.DataFrame()

for economy in APEC_gdp['economy_code'].unique():
    filenames = glob.glob('./data/industry_production/{}/*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df.to_csv('./data/industry_production/industry_subsectors.csv', index = False)