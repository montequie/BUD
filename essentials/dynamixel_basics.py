import json
import time

from butter.mas.api import HttpClient

GOAL_POSITION_REGISTER = 'goal_position'
MOVING_SPEED_REGISTER = 'moving_speed'
GOAL_ACCELERATION_REGISTER = 'goal_acceleration'
PRESENT_POSITION_REGISTER = 'present_position'

TORQUE_REGISTER = 'torque_enable'
TORQUE_OFF = '0'
TORQUE_ON = '1'

CW_ANGLE_LIMIT_REGISTER = 'cw_angle_limit'
CCW_ANGLE_LIMIT_REGISTER = 'ccw_angle_limit'
MULTI_TURN_MODE_DICT = {
    CW_ANGLE_LIMIT_REGISTER: 4095,
    CCW_ANGLE_LIMIT_REGISTER: 4095}
JOINT_MODE_DICT = {
    CW_ANGLE_LIMIT_REGISTER: 0,
    CCW_ANGLE_LIMIT_REGISTER: 4095}


# TODO: maybe rename class?
class Dynamixel(object):

    def __init__(self, motor_names, ip):
        self.motor_names = motor_names
        self.butter_http_client = HttpClient(ip)

    # TODO:
    def go_to_position_in_x_time(self):
        raise NotImplementedError

    def disable_torque(self, motor_names):
        '''
        disable torque for the given motor names
        :type motor_names: [str]
        :return: None
        '''
        if self._are_you_sure('disable torque'):
            for motor_name in motor_names:
                self.butter_http_client.setMotorRegister(motorName=motor_name, registerName=TORQUE_REGISTER,
                                                         value=TORQUE_OFF)
                print('Torque disabled')

    def play_animation(self, animation_name=None):
        '''
        :type animation_name: str
        :return: None
        '''
        if not animation_name:
            # TODO: print animation list
            animation_name = input('Which animation would you like to play? press ENTER\n')
        if self._are_you_sure(F'play animation \'{animation_name}\''):
            self.butter_http_client.playAnimation(animationName=animation_name)

    def get_present_position(self, motor_name):
        '''
        return the present position of a given motor
        :type motor_name:
        :return:
        '''
        return int(
            json.loads(self.butter_http_client.getMotorRegister(motor_name, PRESENT_POSITION_REGISTER).text)['Result'][
            -5:-1].strip())

    def set_multi_turn_mode(self, motor_names):
        '''
        set the given motor names to  multi turn mode
        :type motor_names: [str]
        :return: None
        '''
        for motor_name in motor_names:
            for register_name in MULTI_TURN_MODE_DICT.keys():
                self.butter_http_client.setMotorRegister(motor_name, register_name,
                                                         str(MULTI_TURN_MODE_DICT[register_name]))

    def set_joint_mode(self, motor_names):
        '''
        set the given motor names to joint mode
        :type motor_names: [str]
        :return: None
        '''
        for motor_name in motor_names:
            for register_name in JOINT_MODE_DICT.keys():
                self.butter_http_client.setMotorRegister(motor_name, register_name,
                                                         str(JOINT_MODE_DICT[register_name]))

    # TODO: are you sure to delete _are_you_sure?
    @staticmethod
    def _are_you_sure(action_name):
        # TODO: test print and keyboard not on the same line
        time.sleep(0.01)
        print(F'{action_name}\n')
        return True
