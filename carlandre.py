import pytest
from math import ceil
import sys
from sys import stdout
import os.path



def pop_items(words, num_items):
    ''' Removes num_items from words.'''
    if not words:
         return [], []

    if num_items > len(words):
        raise ValueError('Not enough items!')

    popped = []
    for number in range(num_items):
        removed = words.pop(0)
        popped.append(removed)
    return popped, words

def all_words_less_than(words, maxlength):
    ''' Checks if the words have the correct length given in maxlength'''
    for word in words:
        if len(word) > maxlength:
            return False
    return True

def filterwords(words, maxlength):
    ''' Puts the words which have the correct length in a new list '''
    goodwords = []
    for word in words:
        if len(word) <= maxlength and len(word) >=2:
            goodwords.append(word)
    return goodwords


def pattern(words, maxlength):
    goodwords = filterwords(words, maxlength)
    items_pattern = maxlength + (maxlength -4)

    if len(goodwords) % items_pattern != 0:
        rest = len(goodwords) % items_pattern
        difference = len(goodwords) - rest
        goodwords = goodwords[:difference]

    times = int(len(words) / items_pattern)

    final_pattern = []
    for each_time in range(times):
        popped, whatisleft = pop_items(goodwords, items_pattern)
        if not popped:
            continue
        goodwords = whatisleft

        middle = ceil(len(popped)/2)

        ascending = sorted(popped[:middle], key=len)
        descending = sorted(popped[middle:], key=len, reverse=True)


        sorted_pattern = ascending + descending
        final_pattern.append(sorted_pattern)

    return final_pattern


def test_pattern_returns_list():
    list_items = ['a', 'b', 'c', 'd', 'e']
    assert type(pattern(list_items, 3)) == type([])

def test_pattern_removes_over_max_len():
    list_words_right_length = [['a', 'aa', 'aaa', 'aa', 'a']]
    words_wrong_length = list_words_right_length[0] + ['aaaaa']
    assert pattern(words_wrong_length, 3) == list_words_right_length

def test_pop_items():
    assert pop_items(['a', 'aaa'], 1) == (['a'], ['aaa'])

def test_pop_items_empty_list():
    assert pop_items([], 70) == ([], [])

def test_pop_items_num_too_big():
    with pytest.raises(ValueError):
        pop_items(['a', 'b'], 3)

def test_cuts_for_pattern():
    list_with_nine = ['a'] * 9
    result = pattern(list_with_nine, 3)
    assert len(result[0]) == 5

def test_empty_list_for_pattern():
    result = pattern([], 3)
    assert result == []

def test_list_too_short_for_pattern():
    list_too_short = ['a', 'aa']
    result = pattern(list_too_short, 3)
    assert result == []

if __name__ == '__main__':
    with open('ocr/output.txt', 'r') as handle:
        contents = handle.read()
    splitted = contents.split()
    ll = (pattern(splitted, 8))
    my_list = []
    for l in ll:
        for x in l:
            my_list.append(x)
    joined_list = '\n'.join(my_list)



my_path = '/dev/usb/lp0'
if os.path.exists(my_path):
    sys.stdout = open(my_path, 'w')
    escpos = {
        "init_printer":  "\x1B\x40",
        'papercut':'\x1D\x56\x00',
    }

    emptylines= "\n\n\n\n"
    print(escpos['init_printer'])
    print(joined_list)
    print(emptylines)
    print(escpos['papercut'])
else:
    print(joined_list, '\nThis is all I can do for now, since you don\'t have a printer.')
