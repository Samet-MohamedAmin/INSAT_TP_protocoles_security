import re


class Crypting:
    def __init__(self, src):
        # self.words = Source().words
        self.src = src
        self.crypt_type = 'encrypt'
        self.method = 'cesar_simple'
        self.method_map = {
            'encrypt': {
                'cesar_simple': self.cesar_simple_encrypt,
                'cesar_general': self.cesar_general_encrypt,
                'vigenere': self.vigenere_encrypt},
            'decrypt': {
                'cesar_simple': self.cesar_simple_decrypt,
                'cesar_general': self.cesar_general_decrypt,
                'vigenere': self.vigenere_decrypt}
        }

        self.cesar_simple_key = 3
        self.cesar_general_key = 1
        self.vigenere_key = 'key'

    def say_bla(self):
        print('blaa')

    def crypt(self):
        if self.src.original:
            self.src.normalize()
            self.method_map[self.crypt_type][self.method]()

    def __cesar(self, key):
        """
        cesar encrypting with:
        :param key: decalage des lettres
        """
        begin = ord('a')
        end = ord('z') + 1
        mapping = {i: (i+key-begin) % (end-begin)+begin for i in range(begin, end)}

        self.src.formatted = self.src.formatted.translate(mapping)

    def cesar_simple_encrypt(self):
        self.__cesar(self.cesar_simple_key)

    def cesar_simple_decrypt(self):
        self.__cesar(-self.cesar_simple_key)

    def cesar_general_encrypt(self):
        self.__cesar(self.cesar_general_key)

    def cesar_general_decrypt(self):
        self.__cesar(-self.cesar_general_key)

    def __vigenere(self, direction):
        """
            serves as both encryption and decryption.
            when direction == 1 => encryption;
            when direction == -1 => decryption;
        """
        encrypted_msg = ''
        index_msg = j = 0
        while index_msg < len(self.src.formatted):
            if self.src.formatted[index_msg].isalpha():
                d = direction *(ord(self.vigenere_key.lower()[(index_msg-j) % len(self.vigenere_key.lower())]) - ord('a') + 1)
                encrypted_msg += chr((ord(self.src.formatted[index_msg]) - ord('a') + d) % 26 + ord('a'))
            else:
                j += 1
                encrypted_msg += self.src.formatted[index_msg]
            index_msg += 1
        self.src.formatted = encrypted_msg

    def vigenere_encrypt(self):
        self.__vigenere(1)

    def vigenere_decrypt(self):
        self.__vigenere(-1)



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
