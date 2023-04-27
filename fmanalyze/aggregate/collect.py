import pandas

from fmanalyze.aggregate.color import create_color_roles_dfs, fill_color_dfs
from fmanalyze.attrs.abilities import split_abilities
from fmanalyze.attrs.main_attrs import separate_in_tec_men_phys
from fmanalyze.roles.formation import read_formation, read_formation_for_select


def fill_all_dfs(all_dfs, basedir, formation_df=None, selected_role=None):
    all_octs = pandas.read_csv(f'{basedir}/octs.csv')
    all_gk_octs = pandas.read_csv(f'{basedir}/gk_octs.csv')
    all_attrs = pandas.read_csv(f'{basedir}/all_attrs.csv')
    all_abilities = pandas.read_csv(f'{basedir}/abis.csv')
    if formation_df is not None:
        all_attrs = form_merge(all_attrs, formation_df)
        all_abilities = form_merge(all_abilities, formation_df)
        all_octs = form_merge(all_octs, formation_df)
        all_gk_octs = form_merge(all_gk_octs, formation_df)
    if selected_role is not None:
        all_attrs = all_attrs[all_attrs['Position'] == selected_role]
        all_abilities = all_abilities[all_abilities['Position'] == selected_role]
        all_octs = all_octs[all_octs['Position'] == selected_role]
        all_gk_octs = all_gk_octs[all_gk_octs['Position'] == selected_role]

    all_dfs['octs'] = all_octs
    all_dfs['gk_octs'] = all_gk_octs
    all_dfs['tec'], all_dfs['men'], all_dfs['phys'], all_dfs['goalk'] = separate_in_tec_men_phys(all_attrs)
    all_dfs['tecabi'], all_dfs['menabi'], all_dfs['physabi'] = split_abilities(all_abilities)
    for key, df in all_dfs.items():
        if 'Position' in df.columns:
            temp_column = df.pop('Position')
            df.insert(0, 'Position', temp_column)


def form_merge(ref_df, formation_df):
    ref_df = formation_df.merge(ref_df, on='UID', how='inner')
    if 'Player_y' in ref_df.columns:
        ref_df =ref_df.drop(columns=['Player_y']).rename(columns={'Player_x': 'Player'})
    return ref_df


#        if 'gk' in key:
#            all_dfs[key] = df[df['Position'] == 'GK']
#        else:
#            all_dfs[key] = df[df['Position'] != 'GK']


def create_full_squad_dfs(teamdir, quantilesdir, own_all_dfs, color_dfs, formation=None, selected_role=None):
    formation_file = formation if formation else 'full_squad.csv'
    formation_df = read_formation(teamdir, formation_file, full_squad=True, selected_role=selected_role)
    color_roles_dfs = create_color_roles_dfs(quantilesdir, selected_role=selected_role)
    fill_all_dfs(own_all_dfs, teamdir, formation_df, selected_role)
    fill_color_dfs(color_dfs, own_all_dfs, color_roles_dfs, selected_role)



def create_formation_dfs(teamdir, rivaldir, quantilesdir, formation_df, formation_rival_df, own_all_dfs, color_dfs, rival_all_dfs, rival_color_dfs):

    color_roles_dfs = create_color_roles_dfs(quantilesdir)
    fill_all_dfs(own_all_dfs, teamdir, formation_df)
    fill_color_dfs(color_dfs, own_all_dfs, color_roles_dfs)
    if rivaldir is not None:
        fill_all_dfs(rival_all_dfs, rivaldir, formation_rival_df)
        fill_color_dfs(rival_color_dfs, rival_all_dfs, color_roles_dfs)


def read_formations(teamdir, formation, rivaldir, rivalformation):
    formation_df, formation_rival_df = None, None
    if formation:
        formation_df = read_formation(teamdir, formation)
    else:
        formation_df = read_formation(teamdir, full_squad=True)
    if rivaldir is not None:
        if rivalformation is not None:
            formation_rival_df = read_formation(rivaldir, rivalformation)
        else:
            formation_rival_df = read_formation(rivaldir, full_squad=True)
    return formation_df, formation_rival_df
