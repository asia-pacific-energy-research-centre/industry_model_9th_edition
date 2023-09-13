## Industry modelling for the 9th edition of the APEC Energy Demand and Supply Outlook

This repository houses input data, and builds a model that projects industrial energy consumption for 21 APEC economies out to 2070. 

#### The model (scripts in working development in the workflow folder)
###### Note: input data and results data (csv's, xlsx, etc) is not pushed to git repository. These file types are defined in the .gitignore file. 
###### GDP and population projections to 2100, that form the basis of much of the modelling, are projected and/or packaged here: https://github.com/asia-pacific-energy-research-centre/macro_variables_9th
###### Charts are provided throughout the 'data' and 'results' subfolders. Data is also produced (typically csv's) if you run the scripts on your own machine.

##### Input data (CPB)
- a1_cpb_input_data.py: Open data from CPB Netherlands Bureau for Economic Policy Analysis.
- a2_cpb_data_plots.py: Charts from the above.
##### Industrial GVA input data (WB) and projections to 2100 
- b1_wdi_input_data.py: Builds a function that take World Development Indicators (World Bank) subsector industry data as input and projects these shares of GDP out to 2100.
- b2_wdi_projections.py: Runs the above function with different input choices for all 21 APEC economies
- b3_wdi_consolidation.py: Packages results and outputs charts.
##### Physical production data (World Steel Association, USGS)
- c1_steel_cement_alum.py: Reads in steel, cement and aluminium physical production data.
##### Machine learning scripts
- c2a_steel_projections_ml.py
- c2b_cement_projections_ml.py
- c2c_alum_projections_ml.py

At present, builds OLS, ridge regression, and lasso models using GDP and population projections to 2100. 
The feature variables include combinations of lagged target variables, lagged feature variables, and transformations of these variables (all variables are in log form). Out of the hundreds of models that are built, the models are ranked based on minimising the mean squared error on the test set using k-fold validation (optimal lambda's for RR and Lasso are also selected via k-fold cross validation grid search techniques).
The choice of 'best' model is then a qualitative assessment by the researcher.

- c3_sca_consolidation.py: Consoildates results and outputs various charts.

##### Further refinement of activity/production trajectories
- d1_interim_projections.py: Reads in results from WDI based sector projections and physical production projections (ml methodology), and assigns the projections to the relevant industrial subsectors defined in the Expert Group on Energy Data and Analysis energy data set.
- d2_projection_adjust.py: Defines functions that allows refinement to base level projections obtained above.
- d3_trajectory_refine.py: Executes functions built above for some subsectors in different APEC economies, based on qualitative assessment.
- d4_manual_adjust.py: Allows for bespoke adjusment to production output in specific year(s). Helpful for nowcasting (aligning production with more up to date electricity data, for example), or for deploying a specific project in a specific year (eg new influential factory in year X)
- d5_two_scenarios: Builds additional trajectories of production for selected subsectors (useful for changed critical minerals/materials assumptions) and different material efficiency assumptions in decarbonisation scenarios.
- d6_production_charts.py: Consolidated visualisation of production/activity to this point.

##### Energy data (Expert Group on Energy Data and Analysis APEC energy balance data) 
- e1a_energy_intensity_hist.py: Visualises historical energy intensity (production/activity divided by energy consumption for industrial subsectors)
- e1b_energy_2020.py: Visualises energy mix in 2020 by subsector.
- e2_energy_use_function.py: Defines a function that builds in energy efficiency improvements. That is, the production/activity trajectories grow at a slower rate accouting for selected energy efficiency improvements through time (different choices can be made for different scenarios).
- e3_subsector_energy_intensity.py: Executes above function for each subsector for each economy. Researcher choice of energy intensity improvement uses historical energy intesnity improvement as a guide, amongst other considerations.

##### Energy use projection by subsector
- f1_energy_projection.py: Takes most recent year of energy mix, holds it constant, and then projects out to 2100 using activity/production trajectory that has been lowered based on energy efficiency assumptions. Useful as a conceptual baseline, even though not realistic.

##### Fuel switching
- f2_fuel_switch_function.py

This script defines a function that builds in electrification, a switch to biomass (where applicable), coal-to-gas switching, hydrogen technology deployment (just for steel (DRI processes)), including choice of rate, and when such a switch begins in the projection. Choices can also be made to deploy CCS, via rate and beginning year for chemicals, steel, and non-metallic minerals (cement) subsectors.
- f3_non_energy_switch_function.py

This function enables choices to shift the non-energy sector to more gas or hydrogen (as a feedstock for methanol or ammonia)
- f4_run_fuel_switch_projection.py: Runs the above functions for all economy subsectors. Choices of function inputs (eg electrification, CCS, etc.) are made based on qualitative assessment.
- f5_consolidate_results.py: Consolidates and packages results.
- f6_aggregate_industry.py: Aggregates subfuels and subsectors to comply with required data format, and provides some CCS charts.
- f7_subfuels_industry.py: Provides subfuel detail that is needed by refining and supply models (even though the modelling does not delve to this granularity; uses historical mix in most cases).
- f8_aggregate_non_energy.py: Aggregates subfuels and subsectors to comply with required data format for non-energy results.
- f9_subfuels_industry.py: Provides subfuel detail for non-energy that is needed by refining and supply models.
- f10_biogas_function.py: Defines function that enables a switch from natural gas to biogas if an economy is seeking to incorporate that energy type in their energy policy plans.
- f11_industry_final.py: Deploys biogas function and finalises results dataframe.
- f12_final_charts.py: Provides subsector industry charts for all APEC economies.

##### Other sectors
- g1_coal_transformation.py: Uses modelled coal products consumption to inform projections for coal transformation sector.
- g2_coal_ownuse.py: Provides energy transformation projections for own-use by coke ovens and blast furnaces.

##### Misc
- mlearn_functions.py: Some useful functions that are called by other scripts.
- useful_functions.py: Functions that are called by other scripts.
- z_regressions.py

### Creating the Conda environment for this industry modelling project

Clone this project to your personal computer in a location of your choice.

At the command line, change the directory ('cd') to that selected location.
(So that the cloned project is the working directory.)

Now build the environment that this model operates within by executing:

```bash
$ conda env create --prefix ./env --file ./workflow/envs/environment.yml
```

Once the environment has been created, you can activate it with the following command:

```bash
$ source activate ./env
```

OR (depending on what command line program you're using):

```bash
$ conda activate ./env
```

Note that the `env` directory is *not* under version control as it can always be re-created from 
the `environment.yml` file as necessary.
(i.e. 'env/' is in the .gitignore file)
 
Also note: the environment should automatically activate (as long as you've created as per above) if you're working within VS Code and have chosen the cloned project directory as your working directory.

### Updating the Conda environment

If you add (remove) dependencies to (from) the `environment.yml` file after the environment has 
already been created, then you can update the environment with the following command.

```bash
$ conda env update --prefix ./env --file ./workflow/envs/environment.yml --prune
```

### Listing the full contents of the Conda environment

The list of explicit dependencies for the project are listed in the `environment.yml` file. To see the full list of packages installed into the environment run the following command.

```bash
conda list --prefix ./env
```

