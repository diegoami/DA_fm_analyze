# FOOTBALL MANAGER ANALYZERS

## COMPANION DATA PROJECT   
To check the data structure see the companion project [here](https://github.com/diegoami/DA_fm_data)

## STEPS

1. Import the view `fmf/Important_Attrs_Pos.fmf` into Football Manager
2. Export the stats of your team and your team into your league
3. Set up a yaml file, for instance like the one in `yamls/laliga.yml`, including as the `sourcedir` the location of where you saved your stats files, and as the `targetdir` the location where you want to set up the directory structure for the teams analysis. We will use this file as an example.
4. Run `python3 copy_reports.py -c yamls/laliga.yml` to generate the analysis for all teams. They will be in the `teams` subdirectory of the `targetdir` you specified in the yaml file
5. Run `python3 combine_dfs.py -c yamls/laliga.yml -t` to generate dataset of all players that can play in a roles, that will be put into the `roles` subdirectory of the `targetdir` you specified in the yaml file
6. Run `python3 save_quantiles.py -c yamls/laliga.yml -p` to generate the quantiles for all the attributes, that will be put into the `quantiles` subdirectory of the `targetdir` you specified in the yaml file