# FOOTBALL MANAGER ANALYZERS

## COMPANION DATA PROJECT   
To check the data structure see the companion project [here](https://github.com/diegoami/DA_fm_data)


## IMPORT DATA

1. Import the view `fmf/Important_Attrs_Pos.fmf` into Football Manager
2. Export the stats of your team and your team into your league
3. Set up a yaml file, for instance like the one in `yamls/laliga.yml`, including as the `sourcedir` the location of where you saved your stats files, and as the `targetdir` the location where you want to set up the directory structure for the teams analysis. We will use this file as an example.
4. Run `python3 copy_reports.py -c leagues/laliga.yml` to generate the analysis for all teams. They will be in the `teams` subdirectory of the `targetdir` you specified in the yaml file
5. Run `python3 combine_dfs.py -c leagues/laliga.yml -t` to generate dataset of all players that can play in a roles, that will be put into the `roles` subdirectory of the `targetdir` you specified in the yaml file
6. Run `python3 save_quantiles.py -c leagues/laliga.yml -p` to generate the quantiles for all the attributes, that will be put into the `quantiles` subdirectory of the `targetdir` you specified in the yaml file

## AVAILABLE APPLICATIONS

There are two application that you can start to analyze your squad and the squad of your rival team

* `view_squad.py` to analyze your squad
* `view_formation.py` to analyze a formation

The purpose of each application is to select a list of players and show how they compare to the rest of the league in all attributes. This is done using a color schema highlighting the quantiles of each attribute.

## VIEWING YOUR SQUAD

1. Create a yaml file with the name of the team you want to analyze, as an example check `squads/rsana.yml`
2. Find the `full_squad.csv` file of your team that will be in the `teams` subdirectory of the `targetdir` you specified in the yaml file. It will contain all possible position for your squad, but all lines are commented out
3. (Optional) Make a copy of the `full_squad.csv` file and name it for instance `formation.csv`. Define in the yaml file the `formation` attribute as the name to this file. 
4. Run `python3 view_squad.py -c squads/rsana.yml` to visualize the analysis for your team - select the `squad` button to see the attributes of your squad or formation
5. To filter your squad by position, select the `config` button and select the postion you want to filter by. Use the back button to pick another position.

## VIEWING A FORMATION

1. Create a yaml file containing the name of the teams whose formations you want to analyze, as an example `formations/rsana.yml`
2. Optionally, define and create a formation file containing a subset of `full_squad.csv`, uncommented
3. Alternatively, use the `config` button to select the players you want to analyze - the formation will be saved to other files you define in the yaml file.