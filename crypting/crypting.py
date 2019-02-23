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
    def __init__(self, src):
        # self.words = Source().words
        self.src = src

    def __cesar(self, key):
        """
        cesar encrypting with:
        :param key: decalage des lettres
        """
        begin = ord('a')
        end = ord('z') + 1
        mapping = {i: (i+key-begin) % (end-begin)+begin for i in range(begin, end)}

        self.src.formatted = self.src.formatted.translate(mapping)

    def cesar_encrypt(self, key=3):
        self.__cesar(key)

    def cesar_decrypt(self, key=-3):
        self.__cesar(key)

    def vigenere_encrypt(self, key='vigenereencrypt'):
        key = key.upper()
        formatted = self.src.formatted
        encrypted_msg = ''
        index_msg = 0
        j = 0
        while index_msg < len(formatted):
            if formatted[index_msg].isalpha():
                # NOT sure about adding +1 or NOT !!!
                d = ord(key[(index_msg-j) % len(key)]) - ord('A') + 1
                encrypted_msg += chr((ord(formatted[index_msg]) - ord('A') + d) % 26 + ord('A'))
            else:
                j += 1
                encrypted_msg += formatted[index_msg]
            index_msg += 1
        self.src.formatted = encrypted_msg

    def vigenere_decrypt(self, key='vigenereencrypt'):
        key = key.upper()
        formatted = self.src.formatted
        encrypted_msg = ''
        index_msg = 0
        j = 0
        while index_msg < len(formatted):
            if formatted[index_msg].isalpha():
                # NOT sure about adding +1 or NOT !!!
                d = ord(key[(index_msg - j) % len(key)]) - ord('A') + 1
                encrypted_msg += chr((ord(formatted[index_msg]) - ord('A') - d) % 26 + ord('A'))
            else:
                j += 1
                encrypted_msg += formatted[index_msg]
            index_msg += 1
        self.src.formatted = encrypted_msg



if __name__ == '__main__':
    crypt = Crypting()
    # crypt.cesar_decrypt()
    # crypt.src.print_words()
    # crypt.src.reorder()
    # crypt.src.print_formatted()
    crypt.src.print_formatted()
    crypt.vigenere_encrypt()
    crypt.src.print_formatted()
    crypt.src.extract_words()
    print(crypt.src.words)
    crypt.vigenere_decrypt()
    crypt.src.print_formatted()
    crypt.src.extract_words()
    print(crypt.src.words)
