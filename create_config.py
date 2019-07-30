import json
import os

3
GOAL_POSITION_REGISTER = 'goal_position'
MOVING_SPEED_REGISTER = 'moving_speed'
GOAL_ACCELERATION_REGISTER = 'goal_acceleration'

# config_path = r'/Users/montequie/Dropbox/IDC - CS/miLAB/BUD/configs'
config_path = r'C:\Users\User\PycharmProjects\BUD\configs'

motor_turn_names = ["turnone", "turntwo", "turnthree", "turnfour"]
motor_lean_names = ["leanone", "leantwo", "leanthree", "leanfour"]

fixed_position_dict = {}
for motor_name in motor_turn_names + motor_lean_names:
    fixed_position_dict[motor_name] = {GOAL_ACCELERATION_REGISTER: 1,
                                       MOVING_SPEED_REGISTER: 10,
                                       GOAL_POSITION_REGISTER: 2048,
                                       }


def set_config(config_name='config'):
    config = {}
    config['IP'] = '192.168.0.111'
    config['MOTOR_NAMES'] = motor_turn_names + motor_lean_names
    play_Welcome_New_key = {'key': '1',
                            'module': 'experiment',
                            'function': '_play_animation',
                            'help': 'play animation - Welcome_New',
                            'args': 'Welcome_New'}
    play_Follow_44_key = {'key': '2',
                          'module': 'experiment',
                          'function': '_play_animation',
                          'help': 'play animation - Follow_44',
                          'args': 'Follow_44'}
    play_Attentive_44_key = {'key': '3',
                             'module': 'experiment',
                             'function': '_play_animation',
                             'help': 'play animation - Attentive_44',
                             'args': 'Attentive_44'}
    play_Farewell_New_key = {'key': '4',
                             'module': 'experiment',
                             'function': '_play_animation',
                             'help': 'play animation - Farewell_New',
                             'args': 'Farewell_new'}
    play_Welcome_starting_pose_key = {'key': '5',
                                      'module': 'experiment',
                                      'function': '_play_animation',
                                      'help': 'play animation - Welcome_starting_pose',
                                      'args': 'Welcome_starting_pose'}

    torque_key = {'key': 't',
                  'module': 'experiment',
                  'function': '_disable_torque',
                  'help': 'disable torque for all turn motors',
                  'args': motor_turn_names}
    fix_positions_key = {'key': 'f',
                         'module': 'experiment',
                         'function': '_fix_goal_position',
                         'help': 'fix positions for all turn motors to 0 with minimum speed and acceleration',
                         # TODO: fix also the lean ones?
                         'args': fixed_position_dict}
    config['SHORTCUTS'] = [play_Attentive_44_key, play_Follow_44_key, play_Welcome_New_key, play_Farewell_New_key,
                           play_Welcome_starting_pose_key,
                           torque_key, fix_positions_key]
    with open(os.path.join(config_path, F'{config_name}.json'), 'w') as f:
        json.dump(config, f)
    return os.path.join(config_path, F'{config_name}.json')


def get_config(filename):
    with open(filename) as f:
        return json.load(f)
