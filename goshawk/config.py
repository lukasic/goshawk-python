import yaml

config = {}

def setup(filename):
    with open(filename) as f:
        c = yaml.full_load(f)
        config.update(c)


