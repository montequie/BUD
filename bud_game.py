from butter.mas.api import HttpClient
from db_handler import *
from letter_handler import *
import time

"""
MODULE IMPLEMENTING THE BUD WORD GAME.
"""

# initialize vars and constants.
client = None

JOINT_MAX_VALUE = 4095
FULL_TURN = 4096
FIFTH_OF_A_TURN = 819
THRESHOLD_FOR_LETTER_CORRECT = 409

SIDE_BLANK = 2048
SIDE_ONE = SIDE_BLANK + FIFTH_OF_A_TURN
SIDE_TWO = SIDE_ONE + FIFTH_OF_A_TURN
SIDE_THREE = SIDE_TWO + FIFTH_OF_A_TURN
SIDE_FOUR = SIDE_THREE + FIFTH_OF_A_TURN

DEBUG = True

# main func. for testing
def main():
    print(check_threshold(2048, 2080))


# FUNCTIONS FOR ACTUAL GAMEPLAY.
def start_game(butterClient):
    """
        This function handles the real time gameplay for the bud game.
        It is activated from the WOZ.

    :param butterClient: the butter http client for bud (activated from WOZ)
    :return True - game started without error.
            Error - the exact error that interrupted gameplay.
    """
    # set global client as the HTTP client given !
    global client
    client = butterClient


    # get DB of real words as a list
    db = DB()

    # make RobotLetterConfig
    bud_letter_config = RobotLetterConfig(SIDE_BLANK, 'r', 'e', 'n', 'b')

    print("starting game...") # for testing
    if DEBUG is True:
        while True:
            time.sleep(5)
            print(get_current_state_word(bud_letter_config))

    else:
        # check for change every three seconds.
        while True:

            # var to monitor change in bud's state.
            letter_change = False

            # get bud states with 2 sec diff - to make sure player is waiting idle.
            print("getting word - 1") # for testing
            prev_bud_state = get_current_state_word(bud_letter_config)

            time.sleep(2)

            print("getting word - 2") # for testing
            current_bud_state = get_current_state_word(bud_letter_config)

            # check for letter change
            letter_change = check_letter_change(prev_bud_state, current_bud_state)
            print(f"was there a change - {letter_change}") # for testing


            # if there wasn't a change --> check DB for current state
            if not letter_change:
                print("checking for word in database") # for testing
                result, is_word = db.find_word_in_DB(current_bud_state)

                if is_word:
                    print(f"{result} is a word !") # TODO: play nod animation.
                else:
                    print(f"{result} isnt a word ...")  # TODO: dont play anything and continue.


def check_letter_change(prev_word, current_word):
    """
        checks if a change of letters took place in bud.
    :param prev_word: previous state of bud
    :param current_word: current state of bud
    :return: True - if there was a change.
             False - no change happened.
    """
    return prev_word != current_word


def get_current_state_word(bud_letter_config):
    """

    :param butterClient: the butter http client for bud.
    :param bud_letter_config: the LetterConfig object for current game.
    :return: the word currently displayed on bud.
    """
    global client
    # get motors current positions
    let1_pos = getMotorPos('turnfour')
    let2_pos = getMotorPos('turnthree')
    let3_pos = getMotorPos('turntwo')
    let4_pos = getMotorPos('turnone')

    # get motors corresponding letters
    let1 = bud_letter_config.check_position_for_letter(let1_pos)
    let2 = bud_letter_config.check_position_for_letter(let2_pos)
    let3 = bud_letter_config.check_position_for_letter(let3_pos)
    let4 = bud_letter_config.check_position_for_letter(let4_pos)

    # change to final letter if needed.
    let4 = check_final_letter(let4)

    # create word from letters and return it
    return create_word_from_letters(let1, let2, let3, let4)


# A CLASS FOR CONFIGURATION OF LETTERS ON BUD.

class RobotLetterConfig:
    """
        The RobotLetterConfig object refers to a specific configuration
        of letters for the bud word game.

    """
    def __init__(self, blank_position, letter1, letter2, letter3, letter4):  # blank letter is initialized to be on position 2048.
        """
            every let is a char containing the correct letter.
            letters are entered counter-clockwise from the blank.

        :param let1: first letter (c-clockwise from blank).
        :param let2: second letter (c-clockwise from blank).
        :param let3: third letter (c-clockwise from blank).
        :param let4: fourth letter (c-clockwise from blank).
        """
        # update letter positions to values according to the position given for blank.
        self.update_letter_positions(blank_position)

        # making Letter objects with correct positions.
        self.blank = Letter("", 0)
        self.let1 = Letter(switch_to_hebrew_letter(letter1), 1)
        self.let2 = Letter(switch_to_hebrew_letter(letter2), 2)
        self.let3 = Letter(switch_to_hebrew_letter(letter3), 3)
        self.let4 = Letter(switch_to_hebrew_letter(letter4), 4)

        print(f"blank is {SIDE_BLANK}")
        print(f"{self.let1.char} is {SIDE_ONE}")
        print(f"{self.let2.char} is {SIDE_TWO}")
        print(f"{self.let3.char} is {SIDE_THREE}")
        print(f"{self.let4.char} is {SIDE_FOUR}")

    @staticmethod
    def update_letter_positions(blank_position):
        """
            updates the letter positions global constants
            according to given value for the blank constant.
        :param blank_position: value between 0 - 4095 for the blank.
        """
        # get global vars
        global SIDE_BLANK
        global SIDE_ONE
        global SIDE_TWO
        global SIDE_THREE
        global SIDE_FOUR

        SIDE_BLANK = blank_position % FULL_TURN
        SIDE_ONE = (SIDE_BLANK + FIFTH_OF_A_TURN) % FULL_TURN
        SIDE_TWO = (SIDE_ONE + FIFTH_OF_A_TURN) % FULL_TURN
        SIDE_THREE = (SIDE_TWO + FIFTH_OF_A_TURN) % FULL_TURN
        SIDE_FOUR = (SIDE_THREE + FIFTH_OF_A_TURN) % FULL_TURN

        # for testing
        print("--- LETTER POSITIONS ---")
        print(f"blank is at {SIDE_BLANK}")
        print(f"side 1 is at {SIDE_ONE}")
        print(f"side 2 is at {SIDE_TWO}")
        print(f"side 3 is at {SIDE_THREE}")
        print(f"side 4 is at {SIDE_FOUR}\n")

    def check_position_for_letter(self, current_position):
        """
            returns the current letter that the motor is currently showing,
            according to the configuration of the given 'letters' RobotLettersConfig object.
        :param letters: a RobotLettersConfig object
        :param current_position: the motors current position
        :return: Letter object - refering to the current letter of motor according to its position.
        """
        # normalize motor position to values between 0 - 4095.
        joint_position = get_motor_relative_pos(current_position)
        # test to see positions read
        print(f"position is {joint_position}")
        # iterate through letters to check which corresponds to current position.
        result = check_threshold(self.blank.position, joint_position)
        if result:
            print(f"letter is {self.blank.char}")
            return self.blank.char
        result = check_threshold(self.let1.position, joint_position)
        if result:
            print(f"letter is {self.let1.char}")
            return self.let1.char
        result = check_threshold(self.let2.position, joint_position)
        if result:
            print(f"letter is {self.let2.char}")
            return self.let2.char
        result = check_threshold(self.let3.position, joint_position)
        if result:
            print(f"letter is {self.let3.char}")
            return self.let3.char
        result = check_threshold(self.let4.position, joint_position)
        if result:
            print(f"letter is {self.let4.char}")
            return self.let4.char
        print("letter is UK")
        return "*" # representing 'Unknown'
        # return "somethings wrong, check positions in the letter config object"

    # @staticmethod
    # def check_for_specific_letter(letter, position):
    #     is_letter = check_threshold(letter.position, position)
    #     if is_letter:
    #         return letter.char
    #     return False


# CLASS FOR LETTER OBJECT.
class Letter:
    def __init__(self, char, side):
        self.char = char
        self.side = side
        switcher = {
            0: SIDE_BLANK,
            1: SIDE_ONE,
            2: SIDE_TWO,
            3: SIDE_THREE,
            4: SIDE_FOUR
        }
        self.position = switcher.get(side, "wrong side Exception: side must be between 0 - 4")


# HELPER FUNCTIONS FOR THE GAME.
def get_motor_relative_pos(multi_turn_pos):
    """
        gets the motor's relative position.
        if we regard a full circle as 0 - 4095,
        then 'multi_turn_pos' is between -+28,672.
        So, the function translates the values of multi_turn_pos
        to values between 0 - 4095.

    :param multi_turn_pos: value between -+28,672
    :return: value between 0 - 4095
    """
    if multi_turn_pos == 'Unknown':
        joint_pos = 'Unknown'
    else:
        multi_turn_pos = int(multi_turn_pos)
        # if value is positive, simply use modulo
        if multi_turn_pos > 0:
            joint_pos = int(multi_turn_pos) % FULL_TURN
        else:
            # else, add 4096 until positive, and return
            while multi_turn_pos < 0:
                multi_turn_pos += FULL_TURN
            joint_pos = multi_turn_pos

    return joint_pos


def check_threshold(letter_position, actual_position):
    """
        checks if the current position is within the letter's position.
        threshold is a fifth of a turn. (818 dynamixel units)
    :param letter_position: the position given by the 'word'
    :param actual_position: the motors current position
    :return: True - if motor is within threshold
             False - otherwise (also when given a bad input - Unknown)
    """
    # TODO: why is position Unknown
    if actual_position is 'Unknown':
        return False
    # check for normal diff
    if abs(letter_position - actual_position) < THRESHOLD_FOR_LETTER_CORRECT:
        return True
    # check for special cyclic situations
    # actual_position = abs(actual_position - FULL_TURN)
    # if abs(letter_position - actual_position) < FIFTH_OF_A_TURN:
    #     return True
    return False


def create_word_from_letters(let1, let2, let3, let4):
    """
        gets four chars resembling the four letters
        of current robots' state, and concatenates them to a word (String).
    :param let1: leftmost letter.
    :param let2: middle - left letter.
    :param let3: middle - right letter.
    :param let4: rightmost letter.
    :return: the hebrew word after concatenation (String)
    """

    # assemble word
    word_result = let1 + let2 + let3 + let4
    return word_result


def getMotorPos(motor_name):
    """
        gets motor position.

    :param motor_name: motor name as recorded in Butter Configuration
    :return: the position in dynamixel units (multi - turn)
    """
    global client
    print("multi turn pos")
    print(client.getMotorRegister(motor_name, 'present_position').json()['Result'].split('\t')[1].strip())
    return client.getMotorRegister(motor_name, 'present_position').json()['Result'].split('\t')[1].strip()



# call for main test func.
if __name__ == '__main__':
    main()