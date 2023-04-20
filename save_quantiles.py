import argparse
import os
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

    targetdir = config.get("target_dir", None)
    if targetdir is not None:
        rolesdir = os.path.join(targetdir, 'roles')
        quantilesdir = os.path.join(targetdir, 'quantiles')
        save_stats_for_attrs(rolesdir, quantilesdir, 'attrs')
        save_stats_for_attrs(rolesdir, quantilesdir, 'octs')
        save_stats_for_attrs(rolesdir, quantilesdir, 'abis')

