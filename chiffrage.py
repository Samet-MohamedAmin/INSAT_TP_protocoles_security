from source.source import Source
import re


"""
# chiffrage
## cezar normal 
## cezar généralisé
## véginaire

# dechiffrage
## cezar normal 
## cezar généralisé
## véginaire
### key exist
### key does not exist
"""


class Chiffrage:
    def __init__(self):
        # self.words = Source().words
        self.src = Source()


        self.cesar()


    def cesar(self, key=3):
        begin = ord('A')
        end = ord('Z') + 1
        mapping = {i:(i+key-begin)%(end-begin)+begin for i in range(begin, end)}
        # print(mapping)
        self.src.formatted = self.src.formatted.translate(mapping)

        self.src.print_words()


    def vegenaire(self):
        pass

Chiffrage()