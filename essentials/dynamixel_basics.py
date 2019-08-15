import time

from butter.mas.api import HttpClient

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


class Dynamixel(object):

    def __init__(self, ip):
        self.butterHttpClient = HttpClient(ip)


    def _disable_torque(self, motor_names):
        if self._are_you_sure('disable torque'):
            for motor_name in motor_names:
                self.butterHttpClient.setMotorRegister(motorName=motor_name, registerName=TORQUE_REGISTER,
                                                      value=TORQUE_OFF)
                print('Torque disabled')

    def _play_animation(self, animation_name=None):
        if not animation_name:
            # TODO: print animation list
            animation_name = input('Which animation would you like to play? press ENTER\n')
        if self._are_you_sure(F'play animation \'{animation_name}\''):
            self.butterHttpClient.playAnimation(animationName=animation_name)

    def _set_multi_turn_mode(self, motor_names):
        for motor_name in motor_names:
            for register_name in MULTI_TURN_MODE_DICT.keys():
                self.butterHttpClient.setMotorRegister(motor_name, register_name,
                                                      str(MULTI_TURN_MODE_DICT[register_name]))

    def _set_joint_mode(self, motor_names):
        for motor_name in motor_names:
            for register_name in JOINT_MODE_DICT.keys():
                self.butterHttpClient.setMotorRegister(motor_name, register_name,
                                                      str(JOINT_MODE_DICT[register_name]))

    # TODO: are you sure to delete _are_you_sure?
    @staticmethod
    def _are_you_sure(action_name):
        # TODO: test print and keyboard not on the same line
        time.sleep(0.01)
        print(F'{action_name}\n')
        return True
