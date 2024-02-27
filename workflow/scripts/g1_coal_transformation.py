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
EGEDA_df = pd.read_csv(latest_EGEDA).loc[:,['economy', 'sectors', 'sub1sectors', 'sub2sectors', 'fuels', 'subfuels', '2020', '2021']]\
    .reset_index(drop = True)

EGEDA_coaltrans = pd.read_csv(latest_EGEDA).loc[:,:'2021']
EGEDA_coaltrans = EGEDA_coaltrans.drop(columns = ['is_subtotal']).copy().reset_index(drop = True)

# Vectors to subset
coal_vector = ['01_coal', '02_coal_products']

sector_vector = ['01_production', '02_imports', '03_exports', '06_stock_changes', '09_total_transformation_sector', 
                 '10_losses_and_own_use', '12_total_final_consumption', '14_industry_sector']

sub1sector_vector = ['x', '09_08_coal_transformation', '10_01_own_use', '10_02_transmision_and_distribution_losses']

# Relevant coal transformation
coal_df = EGEDA_df[EGEDA_df['fuels'].isin(coal_vector) & 
                        EGEDA_df['sectors'].isin(sector_vector)].copy()

column_vector = ['economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels']

coal_df = coal_df[(coal_df['sub1sectors'].isin(sub1sector_vector)) & 
                  (coal_df['sub2sectors'] == 'x')][column_vector + ['2020', '2021']]\
    .melt(id_vars = column_vector, var_name = 'year').copy().reset_index(drop = True)

# Coal transformation historical 
EGEDA_coaltrans = EGEDA_coaltrans[(EGEDA_coaltrans['sub1sectors'] == '09_08_coal_transformation') &
                                  (EGEDA_coaltrans['sub2sectors'] == 'x') &
                                  (EGEDA_coaltrans['fuels'].isin(coal_vector))].copy().reset_index(drop = True)

# Grab APEC economies
APEC_economies = pd.read_csv('./data/config/APEC_economies.csv', index_col = 0).squeeze().to_dict()
APEC_economies = list(APEC_economies.keys())[:-7]
# APEC_economies = APEC_economies[5:6]

# Years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

# 2021 and beyond
proj_years = list(range(2021, 2101, 1))
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
    hist_coal_df = hist_coal_df.copy().reset_index(drop = True)

    # Coal TPES
    coaltpes_df = hist_coal_df[(hist_coal_df['fuels'] == '01_coal') &
                               (hist_coal_df['subfuels'] != 'x') &
                               (hist_coal_df['sectors'].isin(['01_production', '02_imports', '03_exports', '06_stock_changes']))].copy().reset_index(drop = True)
    
    min_y2 = coaltpes_df['value'].min() * 1.1
    max_y2 = coaltpes_df['value'].max() * 1.1

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

    min_y3 = coaltrans_df['value'].min() * 1.1
    max_y3 = coaltrans_df['value'].max() * 1.1

    if (len(ref_files) > 0) & (len(tgt_files) > 0): 

        latest_ref = max(ref_files, key = os.path.getctime)
        latest_tgt = max(tgt_files, key = os.path.getctime)

        ref_df = pd.read_csv(latest_ref)
        tgt_df = pd.read_csv(latest_tgt)

        coalp_ref = ref_df[(ref_df['fuels'] == '02_coal_products') &
                        (ref_df['sub1sectors'] == 'x')][['scenarios', 'economy', 'sectors', 'fuels'] + all_years_str]\
                            .melt(id_vars = ['scenarios', 'economy', 'sectors', 'fuels'],
                                var_name = 'year').copy().reset_index(drop = True)
        
        coalp_ref['year'] = coalp_ref['year'].astype(str).astype(int)
        
        coalp_tgt = tgt_df[(tgt_df['fuels'] == '02_coal_products') &
                        (tgt_df['sub1sectors'] == 'x')][['scenarios', 'economy', 'sectors', 'fuels'] + all_years_str]\
                            .melt(id_vars = ['scenarios', 'economy', 'sectors', 'fuels'],
                                var_name = 'year').copy().reset_index(drop = True)
        
        coalp_tgt = coalp_tgt[coalp_tgt['year'].isin(proj_years_str)].copy().reset_index(drop = True)

        coalp_tgt['year'] = coalp_tgt['year'].astype(str).astype(int)
        
        coalp_df = pd.concat([coalp_ref, coalp_tgt]).copy().reset_index(drop = True)

        coalp_df = coalp_df[(coalp_df['year'] >= 2000) &
                            (coalp_df['year'] <= 2070)].copy().reset_index(drop = True)
        
        # Now build in growth for coal transformation (add 2021 data as a beginning to loop through)
        coaltrans_ref = hist_coal_df[(hist_coal_df['sub1sectors'] == '09_08_coal_transformation') &
                                     (hist_coal_df['year'] == 2021)].copy().reset_index(drop = True)

        coaltrans_tgt = hist_coal_df[(hist_coal_df['sub1sectors'] == '09_08_coal_transformation') &
                                     (hist_coal_df['year'] == 2021)].copy().reset_index(drop = True)

        for year in proj_years[1:]:
            # REF
            if coalp_ref.loc[coalp_ref['year'] == (year - 1), 'value'].values[0] == 0:
                ratio_ref = 0
            else:
                ratio_ref = coalp_ref.loc[coalp_ref['year'] == year, 'value'].values[0] / coalp_ref.loc[coalp_ref['year'] == (year - 1), 'value'].values[0]

            addyear_ref = coaltrans_ref[coaltrans_ref['year'] == (year - 1)].copy()
            addyear_ref['value'] = addyear_ref['value'] * ratio_ref
            addyear_ref['year'] = year

            coaltrans_ref = pd.concat([coaltrans_ref, addyear_ref]).copy().reset_index(drop = True)

            # TGT
            if coalp_tgt.loc[coalp_tgt['year'] == (year - 1), 'value'].values[0] == 0:
                ratio_tgt = 0
            else:
                ratio_tgt = coalp_tgt.loc[coalp_tgt['year'] == year, 'value'].values[0] / coalp_tgt.loc[coalp_tgt['year'] == (year - 1), 'value'].values[0]

            addyear_tgt = coaltrans_tgt[coaltrans_tgt['year'] == (year - 1)].copy()
            addyear_tgt['value'] = addyear_tgt['value'] * ratio_tgt
            addyear_tgt['year'] = year

            coaltrans_tgt = pd.concat([coaltrans_tgt, addyear_tgt]).copy().reset_index(drop = True)

        # Now pivot so years are across the top
        coaltrans_wide_ref = coaltrans_ref.pivot(index = ['economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels'], 
                                            columns = 'year', values = 'value').reset_index()
        
        coaltrans_wide_tgt = coaltrans_tgt.pivot(index = ['economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels'], 
                                            columns = 'year', values = 'value').reset_index()
        
        # Historical 
        EGEDA_hist_ref = EGEDA_coaltrans[EGEDA_coaltrans['economy'] == economy].iloc[:,:-1].copy().reset_index(drop = True)
        EGEDA_hist_tgt = EGEDA_hist_ref.copy()
        EGEDA_hist_tgt['scenarios'] = 'target'

        # Final results
        coaltrans_wide_ref = EGEDA_hist_ref.merge(coaltrans_wide_ref, on = ['economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels'], how = 'left')
        coaltrans_wide_tgt = EGEDA_hist_tgt.merge(coaltrans_wide_tgt, on = ['economy', 'sectors', 'sub1sectors', 'fuels', 'subfuels'], how = 'left')

        coaltrans_wide_ref.to_csv(save_location + economy + '_coal_transformation_ref_' + timestamp + '.csv', index = False)
        coaltrans_wide_tgt.to_csv(save_location + economy + '_coal_transformation_tgt_' + timestamp + '.csv', index = False)

        # Add custom fuel column for charting
        ct_chart_ref = coaltrans_wide_ref.melt(id_vars = ['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                                           'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'], var_name = 'year')

        ct_chart_tgt = coaltrans_wide_tgt.melt(id_vars = ['scenarios', 'economy', 'sectors', 'sub1sectors', 'sub2sectors', 
                                                           'sub3sectors', 'sub4sectors', 'fuels', 'subfuels'], var_name = 'year')
        
        ct_chart_ref['fuel'] = np.where(ct_chart_ref['subfuels'] == 'x', ct_chart_ref['fuels'], ct_chart_ref['subfuels'])
        ct_chart_tgt['fuel'] = np.where(ct_chart_tgt['subfuels'] == 'x', ct_chart_tgt['fuels'], ct_chart_tgt['subfuels'])

        ct_chart_ref['year'] = ct_chart_ref['year'].astype(str).astype(int)
        ct_chart_tgt['year'] = ct_chart_tgt['year'].astype(str).astype(int)

        #######################################################################################################
        # Charts
        max_y1 = coalp_df['value'].max() * 1.1
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))
        
        sns.set_theme(style = 'ticks')

        if coalp_df.empty:
            pass

        else:
            sns.lineplot(data = coalp_df,
                        x = 'year',
                        y = 'value',
                        hue = 'scenarios',
                        ax = ax1, 
                        palette = custom_palette)
            
            ax1.set(title = economy + ' coal products industry consumption',
                    xlabel = 'Year',
                    ylabel = 'Petajoules',
                    xlim = (2000, 2070),
                    ylim = (0, max_y1))
            
            ax1.legend(title = '')

            # Projection demarcation
            ax1.axvline(x = 2021, linewidth = 1, linestyle = '--', color = 'black')
        
        if coaltrans_df.empty:
            pass

        else:        
            sns.barplot(data = coaltrans_df,
                        x = 'year',
                        y = 'value',
                        hue = 'fuel',
                        ax = ax2,
                        palette = coal_palette)
            
            ax2.set(title = economy + ' coal transformation',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (min_y3, max_y3))
            
            ax2.legend(title = '', fontsize = 8)

        plt.tight_layout()
        plt.show()

        fig.savefig(save_location + economy + '_coal_products_transformation.png')
        plt.close()
        
        # Next plot of different coal production
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize = (8, 8))

        sns.set_theme(style = 'ticks')

        if coking_df.empty:
            pass
        
        else:
            sns.barplot(data = coking_df,
                        x = 'year',
                        y = 'value',
                        hue = 'sectors',
                        ax = ax1,
                        palette = tpes_palette)
            
            ax1.set(title = economy + ' coking coal production and trade',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (min_y2, max_y2))
            
            ax1.legend(title = '', fontsize = 8)

        if thermal_df.empty:
            pass

        else:
            sns.barplot(data = thermal_df,
                        x = 'year',
                        y = 'value',
                        hue = 'sectors',
                        ax = ax2, 
                        palette = tpes_palette)
            
            ax2.set(title = economy + ' thermal coal production and trade',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                ylim = (min_y2, max_y2))
            
            ax2.legend(title = '', fontsize = 8)
            
        if lignite_df.empty:
            pass

        else:
            sns.barplot(data = lignite_df,
                        x = 'year',
                        y = 'value',
                        hue = 'sectors',
                        ax = ax3,
                        palette = tpes_palette)

            ax3.set(title = economy + ' lignite production and trade',
                    xlabel = 'Year',
                    ylabel = 'Petajoules',
                    ylim = (min_y2, max_y2))
                    
            ax3.legend(title = '', fontsize = 8)

        plt.tight_layout()
        plt.show()

        fig.savefig(save_location + economy + '_coal_production_and_trade.png')
        plt.close()

        # Coal transformation charts
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))

        sns.set_theme(style = 'ticks')

        if ct_chart_ref.empty:
            pass

        else:
            sns.lineplot(data = ct_chart_ref,
                        x = 'year',
                        y = 'value',
                        hue = 'fuel',
                        ax = ax1, 
                        palette = coal_palette)
            
            ax1.set(title = economy + ' coal transformation REF',
                xlabel = 'Year',
                ylabel = 'Petajoules',
                xlim = (2000, 2070))
            
            ax1.legend(title = '')
        
        if ct_chart_tgt.empty:
            pass

        else:
            sns.lineplot(data = ct_chart_tgt,
                        x = 'year',
                        y = 'value',
                        hue = 'fuel',
                        ax = ax2,
                        palette = coal_palette)
        
            ax2.set(title = economy + ' coal transformation TGT',
                    xlabel = 'Year',
                    ylabel = 'Petajoules',
                    xlim = (2000, 2070))

            ax2.legend(title = '', fontsize = 8)

        # Projection demarcation
        ax1.axvline(x = 2021, linewidth = 1, linestyle = '--', color = 'black')
        ax2.axvline(x = 2021, linewidth = 1, linestyle = '--', color = 'black')

        plt.tight_layout()
        plt.show()

        fig.savefig(save_location + economy + '_coal_transformation.png')
        plt.close()

