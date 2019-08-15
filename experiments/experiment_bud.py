import sys

from essentials.create_config import get_config, set_config
from essentials.dynamixel_basics import MOVING_SPEED_REGISTER
from essentials.experiment import Experiment

_THRESHOLD = 25

class BudExperiment(Experiment):
    name = 'BUD'

    def __init__(self, name, stages, config):
        self.name = name
        # self.current_stage_index = 1  # TODO:
        # self.stages = stages  # TODO:
        super().__init__(BudExperiment, config=config)

    def anagram_game(self):
        raise NotImplementedError

    def fix_goal_position(self, fixed_positions):
        '''
        1. toggle between multi-turn to joint mode, avoiding heart attacks
        2. moving to goal fixed positions minimum speed
        :param fixed_positions: dict, keys are motor names, values are dicts of registers and value
        '''
        if self._are_you_sure('fix goal position'):
            self.set_joint_mode(list(fixed_positions.keys()))
            self.set_multi_turn_mode(list(fixed_positions.keys()))
            to_be_fix_motors = []
            for motor_name in fixed_positions.keys():
                for register_name in fixed_positions[motor_name].keys():
                    # TODO: move to dynamixel_basics
                    self.butter_http_client.setMotorRegister(motor_name, register_name,
                                                             str(fixed_positions[motor_name][register_name]))
                # TODO: make it config
                to_be_fix_motors.append((motor_name, 2048))

            while any(to_be_fix_motors):
                for motor_name, fixed_position in to_be_fix_motors:
                    try:
                        if abs(self.get_present_position(motor_name) + _THRESHOLD) >= fixed_position:
                            to_be_fix_motors.remove((motor_name, fixed_position))
                    except:
                        to_be_fix_motors.remove((motor_name, fixed_position))

            for motor_name in fixed_positions.keys():
                self.butter_http_client.setMotorRegister(motor_name, MOVING_SPEED_REGISTER, str(0))
            print('finished fixing')


def main():
    # TODO: test this!
    if sys.argv[1]:
        config_path = set_config(config_name=sys.argv[1])
    stages = []
    experiment = Experiment(name='BUD', stages=stages)
    experiment.run(get_config(sys.argv[1]))


if __name__ == '__main__':
    main()
    # main(config_path=r'C:\Users\User\PycharmProjects\GiMiCHI\configs')
