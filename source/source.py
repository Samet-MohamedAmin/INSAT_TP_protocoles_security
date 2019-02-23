#! /bin/python3 

import re, os


class Source:
    def __init__(self, file_name = 'chiffrage_source.txt'):
        self.file_name = os.path.join('source', file_name)
        self.original = ''
        self.formatted = ''
        self.words = []
        self.mapping_brut = {'à': 'a', 'é': 'e', 'è': 'e', 'ç': 'c'}


        # self.read_from_file()
        # self.normalize()

    def read_from_file(self):
        with open(self.file_name, 'r', encoding='utf-8') as file:
            self.original = file.read()

    def normalize(self):

        # mapping = [('à', 'a'), ('é', 'e'), ('è', 'e'), ('ç', 'c')]
        # mapping = {ord('à'): ord('a'), ord('é'): ord('e'), ord('è'): ord('e')}
        mapping = {ord(x): ord(y) for x, y in self.mapping_brut.items()}

        self.formatted = self.original.lower().translate(mapping)

        # dots dots dots
        self.formatted = re.sub(r'(\W+)', r' \1 ', self.formatted)

    def extract_words(self):
        # get array of words
        self.words = self.formatted.split()

    def print_words(self):
        if not self.words: self.extract_words()
        print(self.words)

    def print_formatted(self):
        print(self.formatted)

    def reorder(self):
        self.formatted = ' '.join(self.words)



result = ''
key = 'chiffrage'

