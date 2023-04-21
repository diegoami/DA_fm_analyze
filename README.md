# FOOTBALL MANAGER ANALYZERS

## COMPANION DATA PROJECT   
To check the data structure see the companion project [here](https://github.com/diegoami/DA_fm_data)

## STEPS

### IMPORT DATA

1. Import the view `fmf/Important_Attrs_Pos.fmf` into Football Manager
2. Export the stats of your team and your team into your league
3. Set up a yaml file, for instance like the one in `yamls/laliga.yml`, including as the `sourcedir` the location of where you saved your stats files, and as the `targetdir` the location where you want to set up the directory structure for the teams analysis. We will use this file as an example.
4. Run `python3 copy_reports.py -c leagues/laliga.yml` to generate the analysis for all teams. They will be in the `teams` subdirectory of the `targetdir` you specified in the yaml file
5. Run `python3 combine_dfs.py -c leagues/laliga.yml -t` to generate dataset of all players that can play in a roles, that will be put into the `roles` subdirectory of the `targetdir` you specified in the yaml file
6. Run `python3 save_quantiles.py -c leagues/laliga.yml -p` to generate the quantiles for all the attributes, that will be put into the `quantiles` subdirectory of the `targetdir` you specified in the yaml file

### VIEWING YOUR SQUAD

1. Create a yaml file with the name of the team you want to analyze, as an example check `teams/rsana.yml`
2. Find the `full_formation.csv` file of your team that will be in the `teams` subdirectory of the `targetdir` you specified in the yaml file. It will contain all possible position for your squad, but all lines are commented out
3. Make a copy of the `full_formation.csv` file and name it for instance `formation.csv`. Comment out the players you want to employ in the next match, with their correspondent role.
4. Define your rival team in the `rival` field of the yaml file
5. Find the `full_formation.csv` file of your rival team and execute the same operation as in the previous step
6. Run `python3 view_squad.py -c teams/rsana.yml` to visualize the analysis for your team as a dash application