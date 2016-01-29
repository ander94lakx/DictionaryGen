# -*- coding: utf-8 -*-

"""Generate a dictionary from one or more files to make dictionary attacks

Output:
    -> "words.txt":         all the words
    -> "combinations.txt":  all the possible uper and lowert case combinations
                            from all the words of the words.txt file
"""

__author__ = 'Ander'
__version__ = '1.0.1.2'
__copyright__ = '(C) 2015 Ander Granado. GNU GPL 3.'

import re as regex
import itertools
import argparse

def delete_HTML(str):
    """Delete the HTML code from a string"""
    # http://stackoverflow.com/questions/3398852/
    p = regex.compile(r'<.*?>')
    return p.sub('', str)

def delete_repeated_words(list):
    """Delete the repeated words of a list"""
    for word in list:
        j = list.index(word) + 1
        while j < len(list):
            if word == list[j]:
                del list[j]
            else:
                j += 1

def _is_number(str):
    try:
        float(str)
    except ValueError:
        return False
    else:
        return True

def upper_lower_combs(list):
    """Get all the upper an lower case letters combination of a word"""
    combs = []
    for word in list:
        if _is_number(word):
            combs.append(word)
        else:
            # http://stackoverflow.com/questions/11144389/
            for elem in map(''.join, itertools.product(*((c.upper(), c.lower()) for c in word))):
                combs.append(elem)
    for elem in combs:
        list.append(elem)


def dict_gen():
    """Generate a dictionary from all the indicated files"""
    # Create all the necessary variables
    dictionary = []
    dictionary_comb = []

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs='+' ,help='Name of the files to take the words')
    parser.add_argument('-k', '--keywords', nargs='+', help='Keywords to generate the dictionary')
    args = parser.parse_args()

    if args.file:
        print('Reading files...')
        for arg in args.file:
            with open(arg, 'r') as file:
                print('\t... reading file: "' + arg + '"')
                if '.txt' in arg:
                    # Convert the file into a single string without line endings
                    # http://stackoverflow.com/questions/8369219/
                    data_str = file.read().replace('\n', ' ')

                    # If is a HTML file, remove all the HTML code
                    if '.html' in arg:
                        data_str = delete_HTML(data_str)

                    # Get all the words of the file (only alphanumerical characters)
                    # http://stackoverflow.com/questions/6181763
                    word_list = regex.sub('[^\w]', ' ',  data_str).split()

                    # Add to the list all the upper lower combinations of every word
                    for word in word_list:
                        dictionary.append(word)
        print('Done reading files.')
        print('Deleting repeated words...')
        delete_repeated_words(dictionary)

    if args.keywords:
        for i in range(1,5):
            words_comb = itertools.permutations(args.keywords, i)
            for word_list in words_comb:
                word_str = ''
                for word in word_list:
                    word_str = word_str + word
                dictionary.append(word_str)

    if not args.file and not args.keywords:
        return

    # Sort the words and make a count of them
    dictionary.sort()
    print('Number of words is:', str(len(dictionary)))

    # Copy all the words in another list
    dictionary_comb = list(dictionary)

    # Generate all the combinations an makes a count of it
    upper_lower_combs(dictionary_comb)
    print('Number of combinations is:', str(len(dictionary_comb)))

    # Write the results on the file
    print('Writing in files...')
    with open("words.txt", 'w') as file:
        for word in dictionary:
            file.write(word + '\n')
    with open("combinations.txt", 'w') as file:
        for word in dictionary_comb:
            file.write(word + '\n')
    print('Done writing.')

if __name__ == "__main__":
    dict_gen()