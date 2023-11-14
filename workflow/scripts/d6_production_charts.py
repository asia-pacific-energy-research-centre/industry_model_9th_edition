# Chart reference and target production trajectories

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
APEC_economy_list = list(APEC_economies.keys())[:-7]
# APEC_economy_list = APEC_economy_list[16:17]

# Energy industry subsectors
industry_sectors = pd.read_csv('./data/EGEDA/industry_egeda.csv', header = None)\
    .squeeze().to_dict()

ind1 = list(industry_sectors.values())[:3]
ind2 = list(industry_sectors.values())[3:]

# The interim modelled production estimates are located here (after adjustment and refinement)
# Interim industry projections

indprod_df = pd.read_csv(latest_prod)
print('Industry production data is from:', prod_date)

nonen_prod_df = pd.read_csv(latest_nonenergy)
print('Non-energy production data is from:', nonenergy_date)

for economy in APEC_economy_list:
    # Where to save charts
    industry_charts = './data/industry_production/7_industry_scenarios_charts/{}/'.format(economy)

    if not os.path.isdir(industry_charts):
        os.makedirs(industry_charts)

    for ind in ind1[:-1]:
        chart_df = indprod_df[(indprod_df['economy_code'] == economy) &
                              (indprod_df['sub1sectors'] == ind)].copy().reset_index(drop = True)
        
        if ind in chart_df['sub1sectors'].unique():
            fig, ax = plt.subplots()

            sns.set_theme(style = 'ticks')

            sns.lineplot(data = chart_df,
                        x = 'year',
                        y = 'value',
                        hue = 'scenario')

            ax.set(title = economy + ' ' + ind,
                xlabel = 'Year',
                ylabel = 'Production index (2017 = 100)',
                ylim = (0, chart_df['value'].max() * 1.1))

            plt.legend(title = '')

            plt.tight_layout()
            plt.show()

            fig.savefig(industry_charts + economy + '_' + ind + '.png')
            
            plt.close()

        else:
            pass

    for ind in ind2:
        chart_df = indprod_df[(indprod_df['economy_code'] == economy) &
                              (indprod_df['sub2sectors'] == ind)].copy().reset_index(drop = True)

        if ind in chart_df['sub2sectors'].unique():
            fig, ax = plt.subplots()

            sns.set_theme(style = 'ticks')

            sns.lineplot(data = chart_df,
                        x = 'year',
                        y = 'value',
                        hue = 'scenario')

            ax.set(title = economy + ' ' + ind,
                xlabel = 'Year',
                ylabel = 'Production index (2017 = 100)',
                ylim = (0, chart_df['value'].max() * 1.1))

            plt.legend(title = '')

            plt.tight_layout()
            plt.show()

            fig.savefig(industry_charts + economy + '_' + ind + '.png')
            
            plt.close()

        else:
            pass


for economy in APEC_economy_list:
    # Where to save charts
    nonenergy_charts = './data/non_energy/5_nonenergy_scenarios_charts/{}/'.format(economy)

    if not os.path.isdir(nonenergy_charts):
        os.makedirs(nonenergy_charts)

    chart_df = nonen_prod_df[(nonen_prod_df['economy_code'] == economy)].copy().reset_index(drop = True)

    if chart_df.empty:
        pass

    else:
        fig, ax = plt.subplots()

        sns.set_theme(style = 'ticks')

        sns.lineplot(data = chart_df,
                    x = 'year',
                    y = 'value',
                    hue = 'scenario')

        ax.set(title = economy + ' non-energy use',
            xlabel = 'Year',
            ylabel = 'Production index (2017 = 100)',
            ylim = (0, chart_df['value'].max() * 1.1))

        plt.legend(title = '')

        plt.tight_layout()
        plt.show()

        fig.savefig(nonenergy_charts + economy + '_non_energy.png')
        
        plt.close()
