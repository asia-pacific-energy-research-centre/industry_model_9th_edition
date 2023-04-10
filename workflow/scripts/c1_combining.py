# Combining data to get trajectories for industrial sector as defined in EGEDA EBT
import os
import re

wanted_wd = 'industry_model_9th_edition'

os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# Run config file
execfile('./config/config_apr2023.py')

# Read in gdp data
APEC_gdp = pd.read_csv('./data/macro/APEC_GDP_population.csv')
APEC_gdp = APEC_gdp[APEC_gdp['variable'] == 'real_GDP'].copy().reset_index(drop = True)

# Read in WDI industry share of GDP (or manufacturing) data
APEC_indshare = pd.read_csv('./data/industry_projection/wdi_projections.csv')
APEC_indshare.series_code.unique()

# Chemical subsector example
for economy in APEC_gdp['economy_code'].unique():
    gdp_data = APEC_gdp[APEC_gdp['economy_code'] == economy].copy().reset_index(drop = True)
    
    manu_share = APEC_indshare[(APEC_indshare['economy_code'] == economy) &
                               (APEC_indshare['series_code'] == 'NV.IND.MANF.ZS')].copy().reset_index(drop = True)
    
    chem_share = APEC_indshare[(APEC_indshare['economy_code'] == economy) &
                               (APEC_indshare['series_code'] == 'NV.MNF.CHEM.ZS.UN')].copy().reset_index(drop = True)
    
    # Now create new series
    chem_data = gdp_data.merge(manu_share, left_on = 'year', right_on = 'year')\
        .merge(chem_share, left_on = 'year', right_on = 'year').dropna().reset_index(drop = True)
    
    if chem_data.empty:
        pass

    else:
        chem_data['chemical production'] = (chem_data['value_x'] * \
            (chem_data['value_y'] / 100) * (chem_data['value'] / 100))
        
        index_year = chem_data.loc[chem_data['year'] == 2018, 'chemical production']\
            .reset_index(drop = True).values[0]
        
        chem_data['indexed'] = chem_data['chemical production'] / index_year * 100
        
        chem_data = chem_data[['economy_code_x', 'economy_x', 'year', 'indexed']].copy()\
            .rename(columns = {'economy_code_x': 'economy_code',
                               'economy_x': 'economy',
                               'indexed': 'value'})
        
        chem_data['series'] = 'Chemical manufacturing index (2010 = 100)'

        chem_data = chem_data[['economy', 'economy_code', 'series', 'year', 'value']].copy()

        fig, ax = plt.subplots()

        sns.set_theme(style = 'ticks')

        sns.lineplot(data = chem_data, 
                        x = 'year',
                        y = 'value',
                        hue = 'series')
        
        ax.set(title = economy,
            xlabel = 'year',
            ylabel = 'Chemical manufacturing')
        
        plt.legend(title = '')
        
        plt.tight_layout()
        #plt.savefig(save_data + economy + '_' + series + '.png')
        plt.show()
        plt.close()