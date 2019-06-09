import os
import json

GOAL_POSITION_REGISTER = 'goal_position'
# TODO: test for correct name
MOVING_SPEED_REGISTER = 'moving_speed'
# TODO: test for correct name
GOAL_ACCELERATION_REGISTER = 'goal_acceleration'

config_path = r'C:\Users\User\PycharmProjects\GiMiCHI\configs'
config_path = r'/Users/montequie/Dropbox/IDC - CS/miLAB/BUD_BUTTER/configs'

motor_turn_names = ["turnone", "turntwo", "turnthree", "turnfour"]
motor_lean_names = ["leanone", "leantwo", "leanthree", "leanfour"]

fixed_position_dict = {}
for motor_turn_name in motor_turn_names:
    fixed_position_dict[motor_turn_name] = {GOAL_POSITION_REGISTER: 0,
                                            MOVING_SPEED_REGISTER: 1,
                                            GOAL_ACCELERATION_REGISTER: 1}


def set_config(config_name='config'):
    config = {}
    config['MOTOR_NAMES'] = motor_turn_names + motor_lean_names
    # TODO: add real animations
    play_animation_key = {'key': 'a',
                          'module': 'experiment',
                          'function': '_play_animation',
                          'args': 'test'}
    torque_key = {'key': 't',
                  'module': 'experiment',
                  'function': '_disable_torque',
                  'args': motor_turn_names}
    fix_positions_key = {'key': 'f',
                         'module': 'experiment',
                         'function': '_fix_goal_position',
                         # TODO: fix also the lean ones?
                         'args': fixed_position_dict}
    config['SHORTCUTS'] = [play_animation_key, torque_key, fix_positions_key]
    with open(os.path.join(config_path, F'{config_name}.json'), 'w') as f:
        json.dump(config, f)
    return os.path.join(config_path, F'{config_name}.json')


def get_config(filename):
    with open(filename) as f:
        return json.load(f)
