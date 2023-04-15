import argparse
import os

from fmanalyze.attrs.instructions import *
from create_dfs import create_dfs_for_basedir
pd.options.mode.chained_assignment = None
import yaml
import shutil


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--config', help='Path to config file', default=None, required=False)
    args = parser.parse_args()
    with open(args.config, 'r') as confhandle:
        config = yaml.safe_load(confhandle)

    sourcedir = config["source_dir"]
    targetdir = config["target_dir"]
    for rtf_filame in os.listdir(sourcedir):
        print(f'Processing {rtf_filame}...')
        dir_to_create = os.path.splitext(rtf_filame)[0]
        basedir = os.path.join(targetdir, dir_to_create)
        os.makedirs(os.path.join(basedir), exist_ok=True)
        shutil.copyfile(os.path.join(sourcedir, rtf_filame), os.path.join(basedir, rtf_filame))
        #os.system(f'cp {os.path.join(sourcedir, rtf_filame)} {os.path.join(basedir, rtf_filame)}')
        print(f'Creating dfs for {basedir}...')
        create_dfs_for_basedir(basedir)