#! /bin/python3

import gi
gi.require_version('Gtk', '3.0')


from gi.repository import Gtk, Gdk, Gio
import os, json
from source.source import Source
from crypting.crypting import Crypting

SEP = ';'
END = '.'

class HandlerEvents:
    def __init__(self, builder):
        self.builder = builder
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.result_buffer = self.builder.get_object('result_text').get_buffer()
        self.text_src = ''
        self.char_mapping = ''

    def open_about(self, widget):
        about_dialog = self.builder.get_object('about_dialog')
        about_dialog.run()
        about_dialog.destroy()


    def update_input(self, input_id, text):
        buffer = self.builder.get_object(input_id).get_buffer()
        buffer.set_text(text)


    def open_dlg(self, title="open file"):
        dlg = Gtk.FileChooserDialog(title=title,
                                    parent=builder.get_object('main_window'),
                                    action=Gtk.FileChooserAction.OPEN)

        dlg.add_buttons(Gtk.STOCK_CANCEL,
                        Gtk.ResponseType.CANCEL,
                        Gtk.STOCK_OPEN,
                        Gtk.ResponseType.OK)
        dlg.run()
        path_base = dlg.get_filename()
        dlg.destroy()

        if path_base:
            with open(path_base) as base_file:
                return base_file.read()

    def open_text_src(self, *args):
        text = self.open_dlg('open text source')
        if text: self.update_input(input_id='input_text_src', text=text)
        self.text_src_updated(text)

    def open_char_mapping(self, *args):
        text = self.open_dlg('open char mapping')
        if text: self.update_input(input_id='input_char_mapping', text=text)
        self.char_mapping_updated(text)

    def paste_text_src(self, widget):
        text = self.clipboard.wait_for_text()
        self.update_input(input_id='input_text_src', text=text)
        self.text_src_updated(text)

    def paste_char_mapping(self, widget):
        text = self.clipboard.wait_for_text()
        self.update_input(input_id='input_char_mapping', text=text)
        self.char_mapping_updated(text)

    def text_src_updated(self, text):
        text_src_image = builder.get_object('result_src_image')
        if text:
            text_src_image.set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)
            self.text_src = text
            self.update_result()
        else:
            text_src_image.set_from_icon_name('gtk-no', Gtk.IconSize.MENU)

    def char_mapping_updated(self, text):
        char_mapping_image = builder.get_object('result_mapping_image')
        if text:
            char_mapping_image.set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)
            self.char_mapping = text
            self.update_result()
        else:
            char_mapping_image.set_from_icon_name('gtk-no', Gtk.IconSize.MENU)


    def update_result(self, *widget):
        source = Source()
        print(self.char_mapping)
        source.mapping_brut = json.loads(self.char_mapping)
        source.original = self.text_src
        source.normalize()
        source.extract_words()
        source.print_words()
        crypt = Crypting(source)
        crypt.cesar_decrypt()
        source.extract_words()
        source.print_words()

    # but_image.set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)



if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file(os.path.join('gui','ui.glade'))

    main_window = builder.get_object('main_window')
    main_window.show_all()

    # load handler events
    handler = HandlerEvents(builder)
    builder.connect_signals(handler)

    # load default char mapping
    with open(os.path.join('source', 'char_mapping_default.json')) as json_data:
        char_mapping = json_data.read()
    handler.char_mapping = char_mapping
    builder.get_object('input_char_mapping').get_buffer().set_text(char_mapping)
    builder.get_object('result_mapping_image')\
        .set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)

    # load default text source
    with open(os.path.join('source','chiffrage_source.txt')) as file:
        text_src = file.read()
    handler.text_src = text_src
    builder.get_object('input_text_src').get_buffer().set_text(text_src)
    builder.get_object('result_src_image')\
        .set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)

    # test crypting
    handler.update_result()

    # connect to destroy event
    main_window.connect("destroy", Gtk.main_quit)
    # start GTK main
    Gtk.main()
    
