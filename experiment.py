import time

import keyboard
from butter.mas.api import HttpClient

from create_config import MOVING_SPEED_REGISTER

TORQUE_REGISTER = 'torque_enable'
TORQUE_OFF = '0'
TORQUE_ON = '1'

CW_ANGLE_LIMIT_REGISTER = 'cw_angle_limit'
CCW_ANGLE_LIMIT_REGISTER = 'ccw_angle_limit'
_MULTI_TURN_MODE_DICT = {
    CW_ANGLE_LIMIT_REGISTER: 4095,
    CCW_ANGLE_LIMIT_REGISTER: 4095}
_JOINT_MODE_DICT = {
    CW_ANGLE_LIMIT_REGISTER: 0,
    CCW_ANGLE_LIMIT_REGISTER: 4095}


def _set_multi_turn_mode(motor_names):
    for motor_name in motor_names:
        for register_name in _MULTI_TURN_MODE_DICT.keys():
            butterHttpClient.setMotorRegister(motor_name, register_name,
                                              str(_MULTI_TURN_MODE_DICT[register_name]))


def _set_joint_mode(motor_names):
    for motor_name in motor_names:
        for register_name in _JOINT_MODE_DICT.keys():
            butterHttpClient.setMotorRegister(motor_name, register_name,
                                              str(_JOINT_MODE_DICT[register_name]))


def _fix_goal_position(fixed_positions):
    '''
    1. toggle between multi-turn to joint mode, avoiding heart attacks
    2. moving to goal fixed positions minimum speed
    :param fixed_positions: dict, keys are motor names, values are dicts of registers and value
    '''
    if _are_you_sure('fix goal position'):
        _set_joint_mode(list(fixed_positions.keys()))
        _set_multi_turn_mode(list(fixed_positions.keys()))
        for motor_name in fixed_positions.keys():
            for register_name in fixed_positions[motor_name].keys():
                butterHttpClient.setMotorRegister(motor_name, register_name,
                                                  str(fixed_positions[motor_name][register_name]))
            butterHttpClient.setMotorRegister(motor_name, MOVING_SPEED_REGISTER, str(0))
            # time.sleep(0.01)
        print('finished fixing')


def _disable_torque(motor_names):
    if _are_you_sure('disable torque'):
        for motor_name in motor_names:
            butterHttpClient.setMotorRegister(motorName=motor_name, registerName=TORQUE_REGISTER, value=TORQUE_OFF)
            print('Torque disabled')


def _play_animation(animation_name=None):
    if not animation_name:
        # TODO: print animation list
        animation_name = input('Which animation would you like to play? press ENTER\n')
    if _are_you_sure(F'play animation \'{animation_name}\''):
        butterHttpClient.playAnimation(animationName=animation_name)


# TODO: are you sure to delete _are_you_sure?
def _are_you_sure(action_name):
    # TODO: test print and keyboard not on the same line
    time.sleep(0.01)
    print(F'{action_name}\n')
    return True

    # run_animation = input(F'are you sure you want to {action_name}? y/n\n')
    # if run_animation.lower() == 'y':
    #     return True
    # else:
    #     return False


def _help(config):
    print('Shortcut keys available:')
    for shortcut in config['SHORTCUTS']:
        key = shortcut['key']
        help = shortcut['help']
        print(f'\r{key} -> {help}')


class Experiment:
    def __init__(self, name, stages):
        self.name = name
        self.current_stage_index = 1
        self.stages = stages
        self.state = True

    def run(self, config):
        global butterHttpClient
        self.config = config
        butter_ip = config['IP']
        butterHttpClient = HttpClient(butter_ip)
        self.init_keyboard_shortcuts(config=config)
        while self.state:
            time.sleep(0.001)

    def __str__(self):
        print(self.name)

    def _quit_experiment(self):
        self.state = False

    def init_keyboard_shortcuts(self, config=None):
        for shortcut in config['SHORTCUTS']:
            import_module = __import__(shortcut['module'])
            key = shortcut['key']
            function_name = shortcut['function']
            args = shortcut['args']
            keyboard.add_hotkey(key, getattr(import_module, function_name), args=(args,))
        # keyboard.add_hotkey('q', self._quit_experiment())
        keyboard.add_hotkey('h', getattr(import_module, '_help'), args=(config,))
