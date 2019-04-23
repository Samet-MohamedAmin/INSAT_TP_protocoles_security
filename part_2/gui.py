#! /bin/python3

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

import hashlib

class Handler:
    def __init__(self, builder):
        self.builder = builder
        self.assistance_window_1 = self.builder.get_object('assistance_window_1')
        self.assistance_window_2 = self.builder.get_object('assistance_window_2')

        self.text_crypted = ''
        self.key = ''
        self.master_key = ''
        self.message_hashed = ''

    def get_current_page(self, assistance_window):
        current_page_index = assistance_window.get_current_page()
        current_page = assistance_window.get_nth_page(current_page_index)

        return current_page

    def set_current_page_complete(self, index, is_page_complete):
        if index == 1: assistance_window = self.assistance_window_1
        elif index == 2: assistance_window = self.assistance_window_2
        
        assistance_window.set_page_complete(self.get_current_page(assistance_window),
                                                    is_page_complete)
    
    def __cesar(self, text, direction):
        key = direction*3
        begin, end = ord('a'), ord('z') + 1
        mapping = {i: (i+key-begin) % (end-begin)+begin for i in range(begin, end)}

        return text.translate(mapping)

    def client_1_encrypt(self, *args):
        text = self.builder.get_object('client_1_word').get_text()
        self.text_crypted = self.__cesar(text, 1)
        self.builder.get_object('client_1_word_encrypted').set_text(self.text_crypted)
        self.builder.get_object('client_2_word_encrypted').set_text(self.text_crypted)

        self.set_current_page_complete(1, True)
        self.set_current_page_complete(2, True)

    def client_2_encrypt(self, *args):
        text = self.builder.get_object('client_2_word').get_text()
        first_text = self.__cesar(self.text_crypted, -1)
        self.key = self.__cesar(first_text + text, 1)
        self.builder.get_object('client_1_key').set_text(self.key)
        self.builder.get_object('client_2_key').set_text(self.key)

        self.set_current_page_complete(1, True)
        # self.set_current_page_complete(2, True)
    
    def hash_key(self, *args):
        self.master_key = hashlib.md5(self.key.encode('utf-8')).hexdigest()
        self.set_current_page_complete(1, True)
        self.builder.get_object('client_1_master_key').set_text(self.master_key)
        self.builder.get_object('client_2_master_key').set_text(self.master_key)

    
    def client_2_send_message(self, *args):
        message = self.builder.get_object('client_2_message_unhashed').get_text()
        self.message_hashed = message
        self.builder.get_object('client_1_message_hashed').set_text(self.message_hashed)
    
    def client_1_unhash(self, *args):
        message_unhashed = self.message_hashed
        self.builder.get_object('client_1_message_unhashed').set_text(message_unhashed)


    def send_token(self, *args):
        self.set_current_page_complete(1, True)
        self.set_current_page_complete(2, True)
    
    def close(self, *args):
        self.quit()

    def quit(self, *args):
        print('quit')
        Gtk.main_quit()



if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file('ui/ui.glade')
    assistance_window_1 = builder.get_object('assistance_window_1')
    assistance_window_2 = builder.get_object('assistance_window_2')

    handler = Handler(builder)
    builder.connect_signals(handler)

    assistance_window_1.show_all()
    assistance_window_2.show_all()


    Gtk.main()

