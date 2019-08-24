import sys
import time

import keyboard

from essentials.dynamixel_basics import Dynamixel


class Experiment(Dynamixel):
    def __init__(self, config, name=None):
        self.state = True
        self.config = config
        self.name = name
        super(Experiment, self).__init__(ip=config['IP'], motor_names=config['MOTOR_NAMES'])

    def run(self):
        self.init_keyboard_shortcuts()
        while self.state:
            time.sleep(0.001)

    def play_sequence(self, sequence):
        for operation in sequence:
            getattr(operation["module"], operation["function"])(operation["args"])
            if "time" in operation:
                time.sleep(int(operation["time"]))

    def _help(self):
        print('Shortcut keys available:')
        for shortcut in self.config['SHORTCUTS']:
            key = shortcut['key']
            help = shortcut['help']
            print(f'\r{key} -> {help}')
        print(f'\rq -> Quit Experiment')

    def _quit_experiment(self):
        self.state = False

    # TODO: change keyboard to something else
    def init_keyboard_shortcuts(self):
        for shortcut in self.config['SHORTCUTS']:
            import_module = __import__(shortcut['module'])
            key = shortcut['key']
            function_name = shortcut['function']
            args = shortcut['args']
            keyboard.add_hotkey(key, getattr(import_module, function_name), args=(args,))
        # TODO: test
        keyboard.add_hotkey('q', self._quit_experiment())
        keyboard.add_hotkey('h', getattr(sys.modules[__name__], self._help().__str__))
