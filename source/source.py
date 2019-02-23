#! /bin/python3 

import re, os, json


class Source:
    def __init__(self,
                 path_mapping='char_mapping_default.json',
                 path_src='chiffrage_source.txt'):
        # self.file_name = os.path.join('source', file_name)
        self.original = ''
        self.formatted = ''
        self.words = []
        self.char_mapping = {} #{'à': 'a', 'é': 'e', 'è': 'e', 'ç': 'c'}
        self.path_mapping = path_mapping
        self.path_src = path_src

        # self.read_from_file()
        # self.normalize()

    def load_char_mapping_from_file(self):
        with open(self.path_mapping, 'r', encoding='utf-8') as file:
            char_mapping_text = file.read()
        self.char_mapping = json.loads(char_mapping_text)
        return char_mapping_text

    def load_text_src_from_file(self):
        with open(self.path_src, 'r', encoding='utf-8') as file:
            self.original = file.read()
        return self.original

    def normalize(self):
        # mapping = [('à', 'a'), ('é', 'e'), ('è', 'e'), ('ç', 'c')]
        # mapping = {ord('à'): ord('a'), ord('é'): ord('e'), ord('è'): ord('e')}
        mapping = {ord(x): ord(y) for x, y in self.char_mapping.items()}

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


