import json
import time

import keyboard

from create_config import MOVING_SPEED_REGISTER
from essentials.dynamixel_basics import Dynamixel

_THRESHOLD = 25


def _help(config):
    print('Shortcut keys available:')
    for shortcut in config['SHORTCUTS']:
        key = shortcut['key']
        help = shortcut['help']
        print(f'\r{key} -> {help}')


class Experiment(Dynamixel):
    def __init__(self, name, stages, config):
        self.name = name
        # self.current_stage_index = 1 # TODO:
        # self.stages = stages # TODO:
        self.state = True
        self.config = config
        super(Experiment, self).__init__(ip=(config['IP']))

    def run(self, config):
        self.init_keyboard_shortcuts(config=config)
        while self.state:
            time.sleep(0.001)

    def __str__(self):
        print(self.name)

    def _quit_experiment(self):
        self.state = False

    # TODO: change keyboard to something else
    @staticmethod
    def init_keyboard_shortcuts(config=None):
        for shortcut in config['SHORTCUTS']:
            import_module = __import__(shortcut['module'])
            key = shortcut['key']
            function_name = shortcut['function']
            args = shortcut['args']
            keyboard.add_hotkey(key, getattr(import_module, function_name), args=(args,))
        # keyboard.add_hotkey('q', self._quit_experiment())
        keyboard.add_hotkey('h', getattr(import_module, '_help'), args=(config,))

    def _fix_goal_position(self, fixed_positions):
        '''
        1. toggle between multi-turn to joint mode, avoiding heart attacks
        2. moving to goal fixed positions minimum speed
        :param fixed_positions: dict, keys are motor names, values are dicts of registers and value
        '''
        if self._are_you_sure('fix goal position'):
            self._set_joint_mode(list(fixed_positions.keys()))
            self._set_multi_turn_mode(list(fixed_positions.keys()))
            to_be_fix_motors = []
            for motor_name in fixed_positions.keys():
                for register_name in fixed_positions[motor_name].keys():
                    self.butterHttpClient.setMotorRegister(motor_name, register_name,
                                                          str(fixed_positions[motor_name][register_name]))
                to_be_fix_motors.append((motor_name, 2048))

            while any(to_be_fix_motors):
                for motor_name, fixed_position in to_be_fix_motors:
                    try:
                        if abs(int(
                                json.loads(self.butterHttpClient.getMotorRegister(motor_name, 'present_position').text)
                                    ['Result'][-5:-1].strip()) + _THRESHOLD) >= fixed_position:
                            to_be_fix_motors.remove((motor_name, fixed_position))
                    except:
                        to_be_fix_motors.remove((motor_name, fixed_position))

            for motor_name in fixed_positions.keys():
                self.butterHttpClient.setMotorRegister(motor_name, MOVING_SPEED_REGISTER, str(0))
            print('finished fixing')
