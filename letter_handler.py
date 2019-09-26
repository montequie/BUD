


def check_final_letter(final_letter):
    """
        checks if final letter needs to be transposed.
        if it should, returns transposed letter.
        if not, returns the same letter.
    :param final_letter: a char in hebrew
    :return: a char in hebrew
    """
    if final_letter == 'מ':
        return 'ם'
    if final_letter == 'נ':
        return 'ן'
    if final_letter == 'צ':
        return 'ץ'
    if final_letter == 'פ':
        return 'ף'
    return final_letter

def switch_to_hebrew_letter(eng_letter):
    """
        gets an english letter, and returns the
        corresponding hebrew letter on the keyboard.
    :param eng_letter: an english char
    :return: the parallel hebrew letter
    """
    switcher = {
        'e': 'ק',
        'r': 'ר',
        't': 'א',
        'y': 'ט',
        'u': 'ו',
        'p': 'פ',
        'a': 'ש',
        's': 'ד',
        'd': 'ג',
        'f': 'כ',
        'g': 'ע',
        'h': 'י',
        'j': 'ח',
        'k': 'ל',
        'z': 'ז',
        'x': 'ס',
        'c': 'ב',
        'v': 'ה',
        'b': 'נ',
        'n': 'מ',
        'm': 'צ',
        ',': 'ת',

    }
    return switcher.get(eng_letter, "NaL")
