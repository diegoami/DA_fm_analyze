POSITION_MAPPINGS = {
    'DCL': 'DC',
    'DCR': 'DC',
    'MCR': 'MC',
    'MCL': 'MC',
    'AMCR': 'AMC',
    'AMCL': 'AMC',
    'STC': 'STC',
    'STCL': 'STC',
    'STCR': 'STC',
    'DMR': 'DM',
    'DML': 'DM'
}

POSITION_SORT_ORDER = [
    'GK',
    'DR',
    'DCR',
    'DC',
    'DCL',
    'DL',
    'WBR',
    'DMR',
    'DM',
    'DML',
    'WBL',
    'MR',
    'MCR',
    'MC',
    'MCL',
    'ML',
    'AMR',
    'AMCR',
    'AMC',
    'AMCL',
    'AML',
    'STCR',
    'STC',
    'STCL'
]

def convert_position(position):
    if position in POSITION_MAPPINGS:
        return POSITION_MAPPINGS[position]
    else:
        return position


def sort_positions(x):
    return POSITION_SORT_ORDER.index(x)