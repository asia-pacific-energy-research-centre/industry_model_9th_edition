# Consolidated grab of steel and cement baseline production estimates

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
gdp_df = pd.read_csv('./data/macro/APEC_GDP_data.csv')
APEC_economies = gdp_df['economy_code'].unique()

# Read in ML results: steel
combined_df = pd.DataFrame()

for economy in APEC_economies:
    filenames = glob.glob('./data/ml_steel/{}/ml_build/model_predictions*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        temp_df['economy_code'] = economy
        temp_df['production'] = 'Steel production'
        temp_df['units'] = 'Thousand tonnes' #WSA source
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df.to_csv('./data/ml_steel/ml_steel_all.csv', index = False)

# Choice of appropriate ML models for each of the economies
steel_model_dict = pd.read_csv('./data/config/ml_baseline_steel.csv', index_col = 0).squeeze().to_dict()

# Save location
steel_save = './data/ml_steel/interim_steel/'

if not os.path.isdir(steel_save):
    os.makedirs(steel_save)

interim_steel_df = pd.DataFrame()

for economy in APEC_economies:
    temp_steel = combined_df[(combined_df['economy_code'] == economy) &
                             (combined_df['model'].isin(['Historic steel production', 
                                                         steel_model_dict[economy]]))]\
                                                            .copy().reset_index(drop = True)
    
    interim_steel_df = pd.concat([interim_steel_df, temp_steel]).copy().reset_index(drop = True)

# Save steel df with selected baseline model results for production 
interim_steel_df.to_csv(steel_save + 'ml_steel_selected.csv', index = False)

# Build some steel charts
for economy in interim_steel_df['economy_code'].unique():
    chart_df = interim_steel_df[(interim_steel_df['economy_code'] == economy) &
                                (interim_steel_df['year'] <= 2070)].copy().reset_index(drop = True)

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                    x = 'year',
                    y = 'steel',
                    hue = 'model')
    
    ax.set(title = economy + ' selected ML steel for baseline production',
            xlabel = 'Year',
            ylabel = 'Steel production (thousand tonnes)')
    
    ax.set_ylim([0, max(chart_df['steel']) * 1.1])
    ax.set_xlim([min(chart_df['year']) - 1, 2070])
    
    plt.legend(title = '')

    plt.tight_layout()
    plt.savefig(steel_save + economy + '_steel_prod.png')
    plt.close()

######################################################################################

# Read in ML results: cement
combined_df = pd.DataFrame()

for economy in APEC_economies:
    filenames = glob.glob('./data/ml_cement/{}/ml_build/model_predictions*.csv'.format(economy))
    for i in filenames:
        temp_df = pd.read_csv(i)
        temp_df['economy_code'] = economy
        temp_df['production'] = 'Cement production'
        temp_df['units'] = 'Thousand tonnes' #USGS source
        combined_df = pd.concat([combined_df, temp_df]).copy()

combined_df.to_csv('./data/ml_cement/ml_cement_all.csv', index = False)

# Choice of appropriate ML models for each of the economies
cement_model_dict = pd.read_csv('./data/config/ml_baseline_cement.csv', index_col = 0).squeeze().to_dict()

# Save location
cement_save = './data/ml_cement/interim_cement/'

if not os.path.isdir(cement_save):
    os.makedirs(cement_save)

interim_cement_df = pd.DataFrame()

for economy in APEC_economies:
    temp_cement = combined_df[(combined_df['economy_code'] == economy) &
                             (combined_df['model'].isin(['Historic cement production', 
                                                         cement_model_dict[economy]]))]\
                                                            .copy().reset_index(drop = True)
    
    interim_cement_df = pd.concat([interim_cement_df, temp_cement]).copy().reset_index(drop = True)

interim_cement_df.to_csv(cement_save + 'ml_cement_selected.csv', index = False)

# Build some cement charts
for economy in interim_cement_df['economy_code'].unique():
    chart_df = interim_cement_df[(interim_cement_df['economy_code'] == economy) &
                                (interim_cement_df['year'] <= 2070)].copy().reset_index(drop = True)

    fig, ax = plt.subplots()

    sns.set_theme(style = 'ticks')

    sns.lineplot(data = chart_df,
                    x = 'year',
                    y = 'cement',
                    hue = 'model')
    
    ax.set(title = economy + ' selected ML cement for baseline production',
            xlabel = 'Year',
            ylabel = 'Cement production (thousand tonnes)')
    
    ax.set_ylim([0, max(chart_df['cement']) * 1.1])
    ax.set_xlim([min(chart_df['year']) - 1, 2070])
    
    plt.legend(title = '')

    plt.tight_layout()
    plt.savefig(cement_save + economy + '_cement_prod.png')
    plt.close()