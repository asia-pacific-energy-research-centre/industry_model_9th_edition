# Finalise industry results with a post hoc biogas switch (from gas to biogas)
# Set working directory to be the project folder 
import os
import re

wanted_wd = 'industry_model_9th_edition'
os.chdir(re.split(wanted_wd, os.getcwd())[0] + wanted_wd)

# execute config file
config_file = './config/config_apr2023.py'
with open(config_file) as infile:
    exec(infile.read())

# Import function
from f10_biogas_function import biogas_switch
# from f10b_hyd_function import hyd_switch

# Modelled years
proj_years = list(range(2021, 2101, 1))

# All years
all_years = list(range(1980, 2101, 1))
all_years_str = [str(i) for i in all_years]

id = ['scenarios', 'economy', 'sectors', 'sub1sectors',	'sub2sectors', 'sub3sectors', 'sub4sectors', 'fuels', 'subfuels']

# Run biogas switch function for relevant economies
# Canada
biogas_switch(economy = '03_CDA', biogas_ref = True, biogas_tgt = True, biogas_rate_ref = 0.001, biogas_rate_tgt = 0.002)

# China
biogas_switch(economy = '05_PRC', biogas_ref = False, biogas_tgt = False)

# Japan
biogas_switch(economy = '08_JPN', biogas_ref = False, biogas_tgt = False)

# Mexico
biogas_switch(economy = '11_MEX', biogas_ref = False, biogas_tgt = False)

# Chinese Taipei
biogas_switch(economy = '18_CT', biogas_ref = False, biogas_tgt = False)

# Thailand
biogas_switch(economy = '19_THA', biogas_ref = False, biogas_tgt = False)

# USA
biogas_switch(economy = '20_USA', biogas_ref = False, biogas_tgt = False)