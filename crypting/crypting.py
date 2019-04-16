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
        begin, end = ord('a'), ord('z') + 1
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
            when direction ==  1 => encryption;
            when direction == -1 => decryption;
        """
        key, formatted = self.vigenere_key.lower(), self.src.formatted
        begin, end = ord('a'), ord('z')+1
        encrypted_msg = ''
        j = 0
        for index, char in enumerate(formatted):
            if char.isalpha():
                d = direction *(ord(key[(index-j) % len(key)]) - begin + 1)
                char = chr((ord(char) - begin + d) % (end - begin) + begin)
            else: j += 1
            encrypted_msg += char
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
