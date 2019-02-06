#! /bin/python3 

import re, os


class Source:
    def __init__(self, file_name = 'chiffrage_source.txt'):
        self.file_name = os.path.join('source', file_name)
        self.original = ''
        self.formatted = ''
        self.words = []

        self.read_from_file()
        self.normalization()

    def read_from_file(self):
        with open(self.file_name, 'r') as file:
            self.original = file.read()

    def normalization(self):
        # mapping = [('à', 'a'), ('é', 'e'), ('è', 'e'), ('ç', 'c')]
        mapping = {ord('à'): ord('a'), ord('é'): ord('e'), ord('è'): ord('e')}

        self.formatted = self.original.translate(mapping)

        # to upper
        self.formatted = self.formatted.upper()

        # dots dots dots
        self.formatted = re.sub(r'(\W+)', r' \1 ', self.formatted)

    def extract_words(self):
        # get array of words
        self.words = self.formatted.split()

    def print_words(self):
        if not self.words: self.extract_words()
        print(self.words)



result = ''
key = 'chiffrage'

