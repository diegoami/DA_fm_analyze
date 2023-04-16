import argparse

import yaml

from fmanalyze.stats.quantiles import save_stats_for_attrs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--config')
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
        exit()
    else:
        with open(args.config, 'r') as confhandle:
            config = yaml.safe_load(confhandle)

    basedir = config["target_dir"]

    save_stats_for_attrs(basedir, 'attrs')
    save_stats_for_attrs(basedir, 'octs')
    save_stats_for_attrs(basedir, 'abis')

