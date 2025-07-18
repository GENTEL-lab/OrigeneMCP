import sys
from pathlib import Path

import toml


root_folder = Path(__file__).parent.parent


def load_toml(fpath: str | Path):
    a = toml.load(open(fpath))
    return a

conf_path = root_folder / "local.conf.toml"
if not conf_path.exists():
    print(f"Please ensure the config file exists: {conf_path}")
    sys.exit(-1)
    
conf = load_toml(conf_path)
