#!/usr/bin/env python

__author__ = "bt3gl"

'''
This program calculate the frequency of letters in a files
so we can use this for cryptoanalysis later.

For example, the 10 most frequent words in english:
e -> 0.104
t -> 0.072
a -> 0.065
0 -> 0.059
n -> 0.056
i -> 0.055
s -> 0.051
r -> 0.049
h -> 0.049
d -> 0.034
'''

import chardet
from collections import defaultdict


# calculate the mean values from the table
def taste_like_english(dict_mean, word):
    mean_word = 0
    counter = 0
    for c in word:
        if c in dict_mean.keys():
            mean_word += dict_mean[c]
            counter += 1
    return mean_word/counter




# count number of letters
def count_letters(FILE):
    dict_letters = defaultdict(int)
    with open(FILE) as file:
        for line in file:
            for word in line.lower().split():
                    for c in word:
                        if c!='!' and c!="," and c!="-" and c!="."\
                         and c!=";" and chardet.detect(c)['encoding'] == 'ascii':
                            dict_letters[c] += 1
    return dict_letters



# calculate the frequency for the letters
def calculate_mean(dict_letters):
    dict_mean = defaultdict(float)
    sum_all = sum(dict_letters.values())
    for letter in sorted(dict_letters.keys()):
        dict_mean[letter] = float(dict_letters[letter])/sum_all
    return dict_mean




# first, test letters with official values
def test_values():
    dict_letters_test = {'e':0.104, 't':0.072, 'a':0.065, 'o':0.059, \
        'n': 0.056, 'i': 0.055, 's':0.051, 'r':0.049, 'h':0.049, 'd':0.034}
    print('Test for "english": ', taste_like_english(dict_letters_test, 'english')) # == 0.045"



# now, test with some file, creating dictionary of letters
def test_file():
    dict_letters = count_letters(FILE)
    dict_mean = calculate_mean(dict_letters)
    for key in sorted(dict_mean, key=dict_mean.get, reverse=True):
        print(key + ' --> ' + str(dict_mean[key]))




if __name__ == '__main__':
    test_values()

    FILE = 'Ariel_Sylvia_Plath.txt'
    test_file()
