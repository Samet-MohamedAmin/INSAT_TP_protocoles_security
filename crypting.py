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


class Crypting:
    def __init__(self):
        # self.words = Source().words
        self.src = Source()

    def __cesar(self, key):
        """
        cesar encrypting with:
        :param key: decalage des lettres
        """
        begin = ord('A')
        end = ord('Z') + 1
        mapping = {i:(i+key-begin)%(end-begin)+begin for i in range(begin, end)}

        self.src.formatted = self.src.formatted.translate(mapping)

    def cesar_encrypt(self, key=3):
        self.__cesar(key)

    def cesar_decrypt(self, key=-3):
        self.__cesar(key)

    def vegenaire(self):
        pass


if __name__ == '__main__':
    crypt = Crypting()
    crypt.cesar_decrypt()
    crypt.src.print_words()
    crypt.src.reorder()
    crypt.src.print_formatted()
