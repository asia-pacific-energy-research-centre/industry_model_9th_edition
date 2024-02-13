# Energy projections by fuels
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Grab industrial production trajectories and also energy data
ind_energy_df = pd.read_csv(latest_inden)
nonenergy_data = pd.read_csv(latest_nonenergy)
EGEDA_df = pd.read_csv(latest_EGEDA)

# Drop column indicator column row from Hyuga and Fin
EGEDA_df = EGEDA_df.drop(columns = ['is_subtotal']).copy().reset_index(drop = True)

EGEDA_df = EGEDA_df.replace({'15_PHL': '15_RP',
                             '17_SGP': '17_SIN'})

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]
economy_select = economy_select[11:12]

# Subset energy data to just 2021
EGEDA_2021_df = EGEDA_df[list(EGEDA_df.iloc[:,:9].columns) + ['2021']]

# Now only keep industry data
EGEDA_ind_2021_df = EGEDA_2021_df[(EGEDA_2021_df['sub1sectors'].str.startswith('14_')) &
                                  (EGEDA_2021_df['sub3sectors'] == 'x') &
                                  (EGEDA_2021_df['subfuels'].isin(['x']))]\
                                    .copy().reset_index(drop = True)

# Convert to long data format
EGEDA_ind_2021_df = EGEDA_ind_2021_df.melt(id_vars = ['economy', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels'],
                                           value_vars = '2021',
                                           var_name = 'year',
                                           value_name = 'energy')

# Ensure year is an integer
EGEDA_ind_2021_df['year'] = EGEDA_ind_2021_df['year'].astype('int') 

# Non-energy 2021
EGEDA_ne_2021_df = EGEDA_2021_df[(EGEDA_2021_df['sectors'].str.startswith('17_')) &
                                  (EGEDA_2021_df['sub1sectors'] == 'x') &
                                  (EGEDA_2021_df['subfuels'].isin(['x']))]\
                                    .copy().reset_index(drop = True)

EGEDA_ne_2021_df = EGEDA_ne_2021_df.melt(id_vars = ['economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels'],
                                         value_vars = '2021',
                                         var_name = 'year',
                                         value_name = 'energy')

# Ensure year is an integer
EGEDA_ne_2021_df['year'] = EGEDA_ne_2021_df['year'].astype('int') 

# Projection years
proj_years = list(range(2022, 2101, 1))

# Fuels of interest 
relevant_fuels = EGEDA_df['fuels'].unique()[[0, 1, 5, 6, 7, 11, 14, 15, 16, 17]]

for economy in economy_select:
    # Save location for charts and data
    save_location = './results/industry/2_energy_projections/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    for sector in ind1[:2] + ind2:
        if sector in ind1: 
            # Historical energy data
            energy_df = EGEDA_ind_2021_df[(EGEDA_ind_2021_df['economy'] == economy) &
                                        (EGEDA_ind_2021_df['sub1sectors'] == sector)]\
                                            .copy().reset_index(drop = True)
            
            # Projected total energy trajectory out to 2100 (reference and target)
            ind_prod_ref = ind_energy_df[(ind_energy_df['economy_code'] == economy) &
                                     (ind_energy_df['sub1sectors'] == sector) &
                                     (ind_energy_df['scenario'] == 'reference')].copy().reset_index(drop = True)
            
            ind_prod_tgt = ind_energy_df[(ind_energy_df['economy_code'] == economy) &
                                     (ind_energy_df['sub1sectors'] == sector) &
                                     (ind_energy_df['scenario'] == 'target')].copy().reset_index(drop = True)
        
        else:
            # Historical energy data
            energy_df = EGEDA_ind_2021_df[(EGEDA_ind_2021_df['economy'] == economy) &
                                          (EGEDA_ind_2021_df['sub2sectors'] == sector)]\
                                            .copy().reset_index(drop = True)
            
            # Projected energy data (manufacturing)
            ind_prod_ref = ind_energy_df[(ind_energy_df['economy_code'] == economy) &
                                         (ind_energy_df['sub2sectors'] == sector) &
                                         (ind_energy_df['scenario'] == 'reference')].copy().reset_index(drop = True)
            
            ind_prod_tgt = ind_energy_df[(ind_energy_df['economy_code'] == economy) &
                                         (ind_energy_df['sub2sectors'] == sector) &
                                         (ind_energy_df['scenario'] == 'target')].copy().reset_index(drop = True)
        
        # Empty data frame to save projections
        energy_proj_ref = pd.DataFrame(columns = energy_df.columns)
        energy_proj_tgt = pd.DataFrame(columns = energy_df.columns)
        
        # Fuel ratio in 2021 dataframe
        fuel_ratio_2021 = energy_df.loc[:, ['fuels', 'energy']]

        # Calculate percentage for each fuel in 2021 and save it in the dataframe    
        for i in range(len(energy_df)):
            fuel_ratio_2021.iloc[i, 1] = energy_df.iloc[i, -1] / \
                energy_df.loc[energy_df['fuels'] == '19_total', 'energy']
        
        if ind_prod_ref.empty:
            pass
        else:
            base_ref = ind_prod_ref.loc[ind_prod_ref['year'] == 2021, 'value'].values[0]

        if ind_prod_tgt.empty:
            pass
        else:
            base_tgt = ind_prod_tgt.loc[ind_prod_tgt['year'] == 2021, 'value'].values[0]

        energy_2021 = energy_df.loc[energy_df['fuels'] == '19_total', 'energy'].values[0]
    
        if ind_prod_ref.empty | ind_prod_tgt.empty:
            pass

        else:
            for year in proj_years:
                temp_ref_df = energy_df.copy().iloc[:-3, :]
                temp_ref_df['year'] = year
                
                temp_tgt_df = energy_df.copy().iloc[:-3, :]
                temp_tgt_df['year'] = year
                
                for fuel in relevant_fuels:
                    # Reference
                    temp_ref_df.loc[temp_ref_df['fuels'] == fuel, 'energy'] = fuel_ratio_2021.loc[fuel_ratio_2021['fuels'] == fuel, 'energy'].values[0] *\
                        energy_2021 * (ind_prod_ref.loc[ind_prod_ref['year'] == year, 'value'].values[0] / base_ref)
                    
                    # Target
                    temp_tgt_df.loc[temp_tgt_df['fuels'] == fuel, 'energy'] = fuel_ratio_2021.loc[fuel_ratio_2021['fuels'] == fuel, 'energy'].values[0] *\
                        energy_2021 * (ind_prod_tgt.loc[ind_prod_tgt['year'] == year, 'value'].values[0] / base_tgt)
                    
                energy_proj_ref = pd.concat([energy_proj_ref, temp_ref_df]).copy().reset_index(drop = True)
                energy_proj_tgt = pd.concat([energy_proj_tgt, temp_tgt_df]).copy().reset_index(drop = True)

            energy_proj_ref.to_csv(save_location + economy + '_' + sector + '_energy_ref.csv', index = False)
            energy_proj_tgt.to_csv(save_location + economy + '_' + sector + '_energy_tgt.csv', index = False)

        # Create some charts
        if energy_proj_ref.empty | energy_proj_tgt.empty:
            pass

        else:
            chart_ref_df = energy_proj_ref.copy().loc[~(energy_proj_ref == 0).any(axis = 1)].reset_index(drop = True)
            chart_ref_df = chart_ref_df[chart_ref_df['year'] <= 2070].copy().reset_index(drop = True)
            chart_tgt_df = energy_proj_tgt.copy().loc[~(energy_proj_tgt == 0).any(axis = 1)].reset_index(drop = True)
            chart_tgt_df = chart_tgt_df[chart_tgt_df['year'] <= 2070].copy().reset_index(drop = True)

            # Pivot the DataFrame
            chart_pivot_ref = chart_ref_df.pivot(index = 'year', columns = 'fuels', values = 'energy')
            chart_pivot_tgt = chart_tgt_df.pivot(index = 'year', columns = 'fuels', values = 'energy')

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))

            sns.set_theme(style = 'ticks')

            chart_pivot_ref.plot.area(ax = ax1,
                                      stacked = True,
                                      alpha = 0.8,
                                      color = fuel_palette1)
            
            chart_pivot_tgt.plot.area(ax = ax2,
                                      stacked = True,
                                      alpha = 0.8,
                                      color = fuel_palette1)
            
            ax1.set(title = economy + ' ' + sector + ' REF',
                    xlabel = 'Year',
                    ylabel = 'Energy (PJ)')
            
            ax2.set(title = economy + ' ' + sector + ' TGT',
                    xlabel = 'Year',
                    ylabel = 'Energy (PJ)')
            
            ax1.legend(title = '', fontsize = 8)
            ax2.legend(title = '', fontsize = 8)
                    
            plt.tight_layout()
            plt.savefig(save_location + economy + '_' + sector + '_energy.png')
            plt.show()
            plt.close()

    ##########################################################################
    # Non-energy portion    
    # Save location for charts and data
    nonenergy_location = './results/non_energy/2_nonenergy_projections/{}/'.format(economy)

    if not os.path.isdir(nonenergy_location):
        os.makedirs(nonenergy_location)

    # Historical energy data
    nonenergy_df = EGEDA_ne_2021_df[(EGEDA_ne_2021_df['economy'] == economy)]\
                                    .copy().reset_index(drop = True)
    
    # Projected total energy trajectory out to 2100 (reference and target)
    ne_prod_ref = nonenergy_data[(nonenergy_data['economy_code'] == economy) &
                                 (nonenergy_data['scenario'] == 'reference')].copy().reset_index(drop = True)
    
    ne_prod_tgt = nonenergy_data[(nonenergy_data['economy_code'] == economy) &
                                 (nonenergy_data['scenario'] == 'target')].copy().reset_index(drop = True)
    
    # Empty data frame to save projections
    nonenergy_proj_ref = pd.DataFrame(columns = nonenergy_df.columns)
    nonenergy_proj_tgt = pd.DataFrame(columns = nonenergy_df.columns)

    # Fuel ratio in 2021 dataframe
    fuel_ratio_2021 = nonenergy_df.loc[:, ['fuels', 'energy']]

    # Calculate percentage for each fuel in 2021 and save it in the dataframe    
    for i in range(len(nonenergy_df)):
        fuel_ratio_2021.iloc[i, 1] = nonenergy_df.iloc[i, -1] / \
            nonenergy_df.loc[nonenergy_df['fuels'] == '19_total', 'energy']
    
    if ne_prod_ref.empty:
        pass
    else:
        base_ref = ne_prod_ref.loc[ne_prod_ref['year'] == 2021, 'value'].values[0]

    if ne_prod_tgt.empty:
        pass
    else:
        base_tgt = ne_prod_tgt.loc[ne_prod_tgt['year'] == 2021, 'value'].values[0]

    nonenergy_2021 = nonenergy_df.loc[nonenergy_df['fuels'] == '19_total', 'energy'].values[0]

    if ne_prod_ref.empty | ne_prod_tgt.empty:
        pass

    else:
        for year in proj_years:
            temp_ref_df = nonenergy_df.copy().iloc[:-3, :]
            temp_ref_df['year'] = year
            
            temp_tgt_df = nonenergy_df.copy().iloc[:-3, :]
            temp_tgt_df['year'] = year
            
            for fuel in relevant_fuels:
                # Reference
                temp_ref_df.loc[temp_ref_df['fuels'] == fuel, 'energy'] = fuel_ratio_2021.loc[fuel_ratio_2021['fuels'] == fuel, 'energy'].values[0] *\
                    nonenergy_2021 * (ne_prod_ref.loc[ne_prod_ref['year'] == year, 'value'].values[0] / base_ref)
                
                # Target
                temp_tgt_df.loc[temp_tgt_df['fuels'] == fuel, 'energy'] = fuel_ratio_2021.loc[fuel_ratio_2021['fuels'] == fuel, 'energy'].values[0] *\
                    nonenergy_2021 * (ne_prod_tgt.loc[ne_prod_tgt['year'] == year, 'value'].values[0] / base_tgt)
                
            nonenergy_proj_ref = pd.concat([nonenergy_proj_ref, temp_ref_df]).copy().reset_index(drop = True)
            nonenergy_proj_tgt = pd.concat([nonenergy_proj_tgt, temp_tgt_df]).copy().reset_index(drop = True)

        nonenergy_proj_ref.to_csv(nonenergy_location + economy + '_non_energy_ref.csv', index = False)
        nonenergy_proj_tgt.to_csv(nonenergy_location + economy + '_non_energy_tgt.csv', index = False)

    # Create some charts
    if nonenergy_proj_ref.empty | nonenergy_proj_tgt.empty:
        pass

    else:
        chart_ref_df = nonenergy_proj_ref.copy().loc[~(nonenergy_proj_ref == 0).any(axis = 1)].reset_index(drop = True)
        chart_ref_df = chart_ref_df[chart_ref_df['year'] <= 2070].copy().reset_index(drop = True)
        chart_tgt_df = nonenergy_proj_tgt.copy().loc[~(nonenergy_proj_tgt == 0).any(axis = 1)].reset_index(drop = True)
        chart_tgt_df = chart_tgt_df[chart_tgt_df['year'] <= 2070].copy().reset_index(drop = True)

        # Pivot the DataFrame
        chart_pivot_ref = chart_ref_df.pivot(index = 'year', columns = 'fuels', values = 'energy')
        chart_pivot_tgt = chart_tgt_df.pivot(index = 'year', columns = 'fuels', values = 'energy')

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))

        sns.set_theme(style = 'ticks')

        chart_pivot_ref.plot.area(ax = ax1,
                                    stacked = True,
                                    alpha = 0.8,
                                    color = fuel_palette1)
        
        chart_pivot_tgt.plot.area(ax = ax2,
                                    stacked = True,
                                    alpha = 0.8,
                                    color = fuel_palette1)
        
        ax1.set(title = economy + ' non-energy REF',
                xlabel = 'Year',
                ylabel = 'Energy (PJ)')
        
        ax2.set(title = economy + ' non-energy TGT',
                xlabel = 'Year',
                ylabel = 'Energy (PJ)')
        
        ax1.legend(title = '', fontsize = 8)
        ax2.legend(title = '', fontsize = 8)
                
        plt.tight_layout()
        plt.savefig(nonenergy_location + economy + '_non_energy.png')
        plt.show()
        plt.close()
