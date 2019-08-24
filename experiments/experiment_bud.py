import sys

from essentials.create_config import get_config, set_config
from essentials.dynamixel_basics import MOVING_SPEED_REGISTER, GOAL_POSITION_REGISTER
from essentials.experiment import Experiment

_THRESHOLD = 25


class BudExperiment(Experiment):
    name = 'BUD'

    def __init__(self, stages, config):
        # self.current_stage_index = 1  # TODO:
        # self.stages = stages  # TODO:
        super().__init__(BudExperiment, config=config)

    def anagram_game(self):
        raise NotImplementedError  # TODO:

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
                self.set_goal_acceleration_speed_position(motor_name, fixed_positions[motor_name])
                to_be_fix_motors.append((motor_name, fixed_positions[motor_name][GOAL_POSITION_REGISTER]))

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
    experiment = BudExperiment(stages=stages, config=get_config('BUD'))
    experiment.run()


if __name__ == '__main__':
    main()
    # main(config_path=r'C:\Users\User\PycharmProjects\GiMiCHI\configs')
