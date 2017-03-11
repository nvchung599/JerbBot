import re
import pickle
import os


def strip(my_str):
    return re.sub(r'\n\s*\n', r'\n\n', my_str.strip(), flags=re.M)

# returns all words in list w/o punctuation, lower cased
def get_words(text):
    word_list = re.compile('\w+').findall(text)
    for i in range(len(word_list)):
        word_list[i] = word_list[i].lower()
    return word_list

# Create new file
def write_file(path, data):
    f = open(path, 'w')
    f.write(data)
    f.close()


def read_file(path):
    f = open(path, 'r')
    return f.read()


# Add content onto existing file
def append_to_file(path, data):
    f = open(path, "a")
    f.write(data + "\n")
    f.close()

# Alternatively...
# with open(path, "a") as f
# f.write(.....


# Delete contents of file
def delete_file_contents(path):
    f = open(path, "w")
    f.close()
    pass

    # TODO when clearing queue, must preserve base url 1st line! (THIS IS THE SEED) /// this is not how this spider works
    # implement new function for this


# Read a file and convert each line to set items
def file_to_set(path):
    my_set = set()
    with open(path, 'rt') as f:
        for line in f:
            # Remove line spacing
            new_line = line.replace('\n', '')

            words_in_line = get_words(new_line)
            for word in words_in_line:
                my_set.add(word)
            # Alternatively... results.add(line.replace('\n',''))
    return my_set


def set_to_file(my_set, path):
    delete_file_contents(path)
    for element in sorted(my_set):
        append_to_file(path, element)


def sort_files():

    paths = ('trunk/filters/essential_body.txt',
            'trunk/filters/excluded_body.txt',
            'trunk/filters/excluded_title.txt')

    for path in paths:
        my_set = set()
        with open(path, 'rt') as f:
            for line in f:
                new_line = line.replace('\n', '')
                my_set.add(new_line.lower())
        set_to_file(my_set, path)


def is_integer(my_str):

    try:
        int(my_str)
        return True
    except:
        return False

def find_bold_number(my_string):
    for i in range(len(my_string)):
        if my_string[i:i + 3] == '<b>':
            elements = get_words(my_string[i:i + 10])
            for element in elements:
                if is_integer(element):
                    return (int(element))

    return 0


# TODO http://opentechschool.github.io/python-data-intro/core/text-files.html