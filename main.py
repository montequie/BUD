from create_config import get_config, set_config
from experiment import Experiment


def main(config_path=None):
    if not config_path:
        config_path = set_config(config_name='BUD')
    # TODO: ask Dina for stages
    stages = []
    experiment = Experiment(name='BUD', stages=stages)
    experiment.run(get_config(config_path))


if __name__ == '__main__':
    main()
