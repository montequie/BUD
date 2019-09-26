# import pandas as pd
# import xlrd
# import os
from openpyxl import load_workbook

FIRST_ROW = 1
LAST_ROW = 23328

# def main():
#     db = DB()
#     w = 'ללח'
#     result, isWord = db.find_word_in_DB(w)
#     print(f"{result} is {isWord} a word")


class DB:

    def __init__(self):
        self.list = get_word_list()

    def find_word_in_DB(self, bud_state):
        for word in self.list:
            if bud_state == word:
                return bud_state, True
        return bud_state, False


def get_word_list():
    wordlist = parse_db_to_wordlist('hebrew_words.xlsx')
    wordlist = filter_words(wordlist)
    return wordlist


def parse_db_to_wordlist(filename):
    wordlist = []
    wb = load_workbook(f"assets/{filename}")
    sheet = wb['Sheet1']
    for cellObj in sheet[f'A{FIRST_ROW}':f'A{LAST_ROW}']:
        for cell in cellObj:
            wordlist.append(cell.value)
    return wordlist


def filter_words(wordlist):
    wordlist = filter_four_letter_words(wordlist)
    return wordlist


def filter_four_letter_words(wordlist):
    filtered_list = []
    for word in wordlist:
        if len(str(word)) < 5:
            filtered_list.append(word)
    return filtered_list

# main()
