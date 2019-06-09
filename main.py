from create_config import get_config, set_config
from experiment import Experiment


def main():
    config_path = set_config(config_name='BUD')
    # config_path = r'C:\Users\User\PycharmProjects\GiMiCHI\configs'
    # config_path = r'/Users/montequie/Dropbox/IDC - CS/miLAB/BUD_BUTTER/configs'
    # config = get_config(os.path.join(config_path, 'config.json'))
    # config = get_config(os.path.join(config_path, 'config_BUD.json'))

    stages = []
    experiment = Experiment(name='BUD', stages=stages)
    experiment.run(get_config(config_path))


if __name__ == '__main__':
    main()
