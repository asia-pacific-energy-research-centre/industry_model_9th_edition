# Consolidate results ready for integration
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Only use 21 APEC economies (economy_list defined in config file)
economy_select = economy_list[:-7]
# Only run one economy
economy_select = economy_list[2:3]

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# Fuels
others_fuels = ['16_02_industrial_waste', '16_03_municipal_solid_waste_renewable',
                '16_04_municipal_solid_waste_nonrenewable', '16_05_biogasoline', 
                '16_06_biodiesel', '16_08_other_liquid_biofuels', '16_09_other_sources', 
                '16_x_ammonia']

wanted_fuels = pd.read_csv('./data/config/fuels_to_chart1.csv', header = 0)
wanted_fuels = pd.Series(wanted_fuels.fuel.values, index = wanted_fuels.fuels).to_dict()

# Read in steel data
for economy in list(economy_select):
    # Save location for charts and data
    save_location = './results/industry/5_final/{}/charts/'.format(economy)

    if not os.path.isdir(save_location):
        os.makedirs(save_location)

    data_location = './results/industry/5_final/{}/'.format(economy)

    ref_prefix = economy + '_industry_ref_'
    tgt_prefix = economy + '_industry_tgt_'

    ref_files = glob.glob(data_location + ref_prefix + '*.csv')
    tgt_files = glob.glob(data_location + tgt_prefix + '*.csv')

    if (len(ref_files) > 0) & (len(tgt_files) > 0): 

        latest_ref = max(ref_files, key = os.path.getctime)
        latest_tgt = max(tgt_files, key = os.path.getctime)

        ref_df = pd.read_csv(latest_ref)
        tgt_df = pd.read_csv(latest_tgt)

        relevant_2sectors = np.delete(ref_df['sub2sectors'].unique(),
                                          np.where(ref_df['sub2sectors'].unique() == 'x'))
        
        relevant_1sectors = np.delete(ref_df['sub1sectors'].unique(),
                                          np.where(ref_df['sub1sectors'].unique() == '14_03_manufacturing'))

        for sector in list(relevant_1sectors) + list(relevant_2sectors):
            if sector in relevant_2sectors:
                chart_ref_df = ref_df[(ref_df['sub2sectors'] == sector) &
                                      (ref_df['sub3sectors'] == 'x')]
                
                chart_tgt_df = tgt_df[(tgt_df['sub2sectors'] == sector) &
                                      (tgt_df['sub3sectors'] == 'x')]
                
            elif sector in relevant_1sectors:
                chart_ref_df = ref_df[(ref_df['sub1sectors'] == sector) &
                                      (ref_df['sub2sectors'] == 'x')]
                
                chart_tgt_df = tgt_df[(tgt_df['sub1sectors'] == sector) &
                                      (tgt_df['sub2sectors'] == 'x')]
            
            # Now just keep the data wanted and reshape
            # REF
            chart_ref_df = chart_ref_df.drop(['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                              'sub3sectors', 'sub4sectors'], axis = 1)\
                                                .melt(id_vars = ['sub2sectors', 'fuels', 'subfuels'],
                                                      var_name = 'year',
                                                      value_name = 'energy')\
                                                    .copy().reset_index(drop = True)
            
            chart_ref_df['year'] = chart_ref_df['year'].astype('int')

            chart_ref_df = chart_ref_df[(chart_ref_df['year'] <= 2070) &
                                        (chart_ref_df['year'] >= 2000) &
                                        (chart_ref_df['energy'] != 0) &
                                        (chart_ref_df['fuels'] != '19_total')].copy().reset_index(drop = True)
            
            chart_ref_df = chart_ref_df.fillna(0)
            chart_ref_df['fuel'] = np.nan

            chart_ref_df['fuel'] = np.where(chart_ref_df['subfuels'] == 'x', 
                                            chart_ref_df['fuels'], chart_ref_df['subfuels'])

            for year in chart_ref_df['year'].unique():
                others_agg = chart_ref_df[(chart_ref_df['year'] == year) & 
                                          (chart_ref_df['subfuels'].isin(others_fuels))]\
                                            .groupby(['sub2sectors', 'fuels', 'year']).sum()\
                                            .reset_index().assign(fuel = '16_x_others')

                chart_ref_df = pd.concat([chart_ref_df, others_agg]).copy().reset_index(drop = True)

            chart_ref_df = chart_ref_df[chart_ref_df['fuel'].isin(wanted_fuels.keys())].copy().reset_index(drop = True)

            new_ref_df = chart_ref_df.pivot(index = 'year', columns = 'fuel', values = 'energy')

            # TGT
            chart_tgt_df = chart_tgt_df.drop(['scenarios', 'economy', 'sectors', 'sub1sectors', 
                                              'sub3sectors', 'sub4sectors'], axis = 1)\
                                                .melt(id_vars = ['sub2sectors', 'fuels', 'subfuels'],
                                                      var_name = 'year',
                                                      value_name = 'energy')\
                                                    .copy().reset_index(drop = True)
            
            chart_tgt_df['year'] = chart_tgt_df['year'].astype('int')

            chart_tgt_df = chart_tgt_df[(chart_tgt_df['year'] <= 2070) &
                                        (chart_tgt_df['year'] >= 2000) &
                                        (chart_tgt_df['energy'] != 0) &
                                        (chart_tgt_df['fuels'] != '19_total')].copy().reset_index(drop = True)
            
            chart_tgt_df = chart_tgt_df.fillna(0)
            chart_tgt_df['fuel'] = np.nan

            chart_tgt_df['fuel'] = np.where(chart_tgt_df['subfuels'] == 'x', 
                                            chart_tgt_df['fuels'], chart_tgt_df['subfuels'])

            for year in chart_tgt_df['year'].unique():
                others_agg = chart_tgt_df[(chart_tgt_df['year'] == year) & 
                                          (chart_tgt_df['subfuels'].isin(others_fuels))]\
                                            .groupby(['sub2sectors', 'fuels', 'year']).sum()\
                                            .reset_index().assign(fuel = '16_x_others')

                chart_tgt_df = pd.concat([chart_tgt_df, others_agg]).copy().reset_index(drop = True)

            chart_tgt_df = chart_tgt_df[chart_tgt_df['fuel'].isin(wanted_fuels.keys())].copy().reset_index(drop = True)

            new_tgt_df = chart_tgt_df.pivot(index = 'year', columns = 'fuel', values = 'energy')

            # Define locations for chart index and custom labels
            max_y = 1.1 * max(chart_ref_df.groupby('year')['energy'].sum().max(), chart_tgt_df.groupby('year')['energy'].sum().max())
            proj_location = 0.925 * max_y

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize = (8, 8))

            sns.set_theme(style = 'ticks')

            if new_ref_df.empty | new_tgt_df.empty:
                pass
            
            else:
                new_ref_df.plot.area(ax = ax1,
                                    stacked = True,
                                    #alpha = 0.8,
                                    color = fuel_palette1,
                                    linewidth = 0)
                
                new_tgt_df.plot.area(ax = ax2,
                                    stacked = True,
                                    #alpha = 0.8,
                                    color = fuel_palette1,
                                    linewidth = 0)
                
                if sector == 'x':
                    chart_title_ref = economy + ' industrial energy consumption REF'
                else:
                    chart_title_ref = economy + ' ' + sector + ' energy consumption REF'

                if sector == 'x':
                    chart_title_tgt = economy + ' industrial energy consumption TGT'
                else:
                    chart_title_tgt = economy + ' ' + sector + ' energy consumption TGT'

                ax1.set(title = chart_title_ref,
                        xlabel = 'Year',
                        ylabel = 'Energy (PJ)',
                        xlim = (2000, 2070),
                        ylim = (0, max_y))
                
                ax2.set(title = chart_title_tgt,
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
                # ax1.get_legend().remove()
                # ax2.get_legend().remove()

                plt.tight_layout()
                if sector == 'x':
                    plt.savefig(save_location + economy + '_14_industry_sector.png')
                else:
                    plt.savefig(save_location + economy + '_' + sector + '.png')
                plt.show()
                plt.close()
            
