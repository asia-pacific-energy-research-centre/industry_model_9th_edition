# Coal transformation analysis
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# latest EGEDA data
EGEDA_df = pd.read_csv(latest_EGEDA).loc[:,['economy', 'sectors', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels', '2019', '2020']]\
    .reset_index(drop = True)

coal_vector = ['01_coal', '02_coal_products']

sector_vector = ['01_production', '02_imports', '03_exports', '06_stock_changes', '09_total_transformation_sector', 
                 '10_losses_and_own_use', '12_total_final_consumption', '14_industry_sector']

sub1sector_vector = ['x', '09_08_coal_transformation', '10_01_own_use', '10_02_transmision_and_distribution_losses']

# Relevant coal transformation
coal_df = EGEDA_df[EGEDA_df['fuels'].isin(coal_vector) & 
                        EGEDA_df['sectors'].isin(sector_vector)].copy()

column_vector = ['economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels']

coal_df = coal_df[(coal_df['sub1sectors'].isin(sub1sector_vector)) & 
                  (coal_df['sub2sectors'] == 'x')][column_vector + ['2019', '2020']]\
    .melt(id_vars = column_vector, var_name = 'year').copy().reset_index(drop = True)

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()
APEC_economies = list(APEC_economies.keys())[:-7]

# Years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

# 2020 and beyond
proj_years = list(range(2020, 2101, 1))
proj_years_str = [str(i) for i in proj_years]

for economy in APEC_economies:
    # Save location
    save_location = './results/coal_transformation/{}/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    modelled_result = './results/industry/5_final/{}/'.format(economy)

    ref_prefix = economy + '_industry_ref_'
    tgt_prefix = economy + '_industry_tgt_'

    ref_files = glob.glob(modelled_result + ref_prefix + '*.csv')
    tgt_files = glob.glob(modelled_result + tgt_prefix + '*.csv')

    #################################################################
    # Historical data
    hist_coal_df = coal_df[coal_df['economy'] == economy].copy().reset_index(drop = True)

    hist_coal_df['year'] = hist_coal_df['year'].astype(str).astype(int)
    hist_coal_df = hist_coal_df[(hist_coal_df['year'] >= 2000) &
                                (hist_coal_df['year'] <= 2070)].copy().reset_index(drop = True)

    # Coal TPES
    coaltpes_df = hist_coal_df[(hist_coal_df['fuels'] == '01_coal') &
                               (hist_coal_df['subfuels'] != 'x') &
                               (hist_coal_df['sectors'].isin(['01_production', '02_imports', '03_exports', '06_stock_changes']))].copy().reset_index(drop = True)
    
    min_y2 = coaltpes_df['value'].min() * 1.4
    max_y2 = coaltpes_df['value'].max() * 1.4

    coking_df = coaltpes_df[coaltpes_df['subfuels'] == '01_01_coking_coal'].copy().reset_index(drop = True)
    thermal_df = coaltpes_df[coaltpes_df['subfuels'] == '01_x_thermal_coal'].copy().reset_index(drop = True)
    lignite_df = coaltpes_df[coaltpes_df['subfuels'] == '01_05_lignite'].copy().reset_index(drop = True)

    # Coal transformation
    coaltrans_df1 = hist_coal_df[(hist_coal_df['sub1sectors'] == '09_08_coal_transformation') &
                                 (hist_coal_df['subfuels'] != 'x')]
    
    coaltrans_df2 = hist_coal_df[(hist_coal_df['sub1sectors'] == '09_08_coal_transformation') &
                                 (hist_coal_df['fuels'] == '02_coal_products')]
    
    coaltrans_df = pd.concat([coaltrans_df1, coaltrans_df2]).copy().reset_index(drop = True)

    coaltrans_df['fuel'] = np.where(coaltrans_df['subfuels'] == 'x', coaltrans_df['fuels'], coaltrans_df['subfuels'])

    min_y3 = coaltrans_df['value'].min() * 1.4
    max_y3 = coaltrans_df['value'].max() * 1.4

    if (len(ref_files) > 0) & (len(tgt_files) > 0): 

        latest_ref = max(ref_files, key = os.path.getctime)
        latest_tgt = max(tgt_files, key = os.path.getctime)

        ref_df = pd.read_csv(latest_ref)
        tgt_df = pd.read_csv(latest_tgt)

        coalp_ref = ref_df[(ref_df['fuels'] == '02_coal_products') &
                        (ref_df['sub1sectors'] == 'x')][['scenarios', 'economy', 'sectors', 'fuels'] + all_years_str]\
                            .melt(id_vars = ['scenarios', 'economy', 'sectors', 'fuels'],
                                var_name = 'year').copy().reset_index(drop = True)
        
        coalp_tgt = tgt_df[(tgt_df['fuels'] == '02_coal_products') &
                        (tgt_df['sub1sectors'] == 'x')][['scenarios', 'economy', 'sectors', 'fuels'] + all_years_str]\
                            .melt(id_vars = ['scenarios', 'economy', 'sectors', 'fuels'],
                                var_name = 'year').copy().reset_index(drop = True)
        
        coalp_tgt = coalp_tgt[coalp_tgt['year'].isin(proj_years_str)].copy().reset_index(drop = True)
        
        coalp_df = pd.concat([coalp_ref, coalp_tgt]).copy().reset_index(drop = True)

        coalp_df['year'] = coalp_df['year'].astype(str).astype(int)
        coalp_df = coalp_df[(coalp_df['year'] >= 2000) &
                            (coalp_df['year'] <= 2070)].copy().reset_index(drop = True)

        #######################################################################################################
        max_y1 = coalp_df['value'].max() * 1.1
        proj_location = 0.925 * max_y1
        
        fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize = (8, 8))

        sns.set_theme(style = 'ticks')

        sns.lineplot(data = coalp_df,
                     x = 'year',
                     y = 'value',
                     hue = 'scenarios',
                     ax = ax1, 
                     palette = custom_palette)
        
        sns.barplot(data = coaltrans_df,
                    x = 'year',
                    y = 'value',
                    hue = 'fuel',
                    ax = ax2,
                    palette = coal_palette)
        
        sns.barplot(data = coking_df,
                    x = 'year',
                    y = 'value',
                    hue = 'sectors',
                    ax = ax4,
                    palette = tpes_palette)
        
        sns.barplot(data = thermal_df,
                    x = 'year',
                    y = 'value',
                    hue = 'sectors',
                    ax = ax5, 
                    palette = tpes_palette)
        
        sns.barplot(data = lignite_df,
                    x = 'year',
                    y = 'value',
                    hue = 'sectors',
                    ax = ax6,
                    palette = tpes_palette)

        ax1.set(title = economy + ' coal products industry consumption',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                xlim = (2000, 2070),
                ylim = (0, max_y1))
        
        ax2.set(title = economy + ' coal transformation',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (min_y3, max_y3))
        
        ax4.set(title = economy + ' coking coal production and trade',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (min_y2, max_y2))
        
        ax5.set(title = economy + ' thermal coal production and trade',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (min_y2, max_y2))
        
        ax6.set(title = economy + ' lignite production and trade',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (min_y2, max_y2))

        ax1.legend(title = '')
        ax2.legend(title = '', fontsize = 8)
        ax4.legend(title = '', fontsize = 8)
        ax5.legend(title = '', fontsize = 8)
        ax6.legend(title = '', fontsize = 8)

        # Projection demarcation
        ax1.axvline(x = 2020, linewidth = 1, linestyle = '--', color = 'black')

        plt.tight_layout()
        plt.show()

        # fig.savefig(industry_charts + economy + '_' + ind + '.png')
        
        plt.close()