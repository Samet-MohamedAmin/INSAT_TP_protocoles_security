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
    def __init__(self, builder, source=Source()):
        self.builder = builder
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.result_buffer = self.builder.get_object('result_text').get_buffer()
        self.source = source

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
        if text:
            self.update_input(input_id='input_text_src', text=text)
            self.text_src_updated(text)

    def open_char_mapping(self, *args):
        text = self.open_dlg('open char mapping')
        if text:
            self.update_input(input_id='input_char_mapping', text=text)
            self.char_mapping_updated()

    def paste_text_src(self, widget):
        text = self.clipboard.wait_for_text()
        self.update_input(input_id='input_text_src', text=text)
        self.text_src_updated(text)

    def paste_char_mapping(self, widget):
        text = self.clipboard.wait_for_text()
        self.update_input(input_id='input_char_mapping', text=text)
        self.char_mapping_updated()

    def text_src_updated(self):
        text_src_image = builder.get_object('result_src_image')
        text_src_image.set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)
        self.update_result()

    def char_mapping_updated(self):
        char_mapping_image = builder.get_object('result_mapping_image')
        if self.source.char_mapping:
            char_mapping_image.set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)
            self.update_result()
        else:
            char_mapping_image.set_from_icon_name('gtk-no', Gtk.IconSize.MENU)

    def params_vegenaire_changed(self, widget):
        print(widget.get_text())

    def update_result(self, *widget):
        print('update result')
        print(self.source.original)
        print('_'*20)
        if self.source.original:
            self.source.normalize()
            self.source.extract_words()
            self.source.print_words()
            crypt = Crypting(self.source)
            crypt.cesar_decrypt()
            self.update_input(input_id='result_text', text=self.source.reorder())
            # self.source.extract_words()
            # self.source.print_words()


if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file(os.path.join('gui','ui.glade'))

    main_window = builder.get_object('main_window')
    main_window.show_all()

    # create Source() object
    src = Source(path_mapping=os.path.join('source', 'char_mapping_default.json'),
                 path_src=os.path.join('source', 'chiffrage_source.txt'))

    # load handler events
    handler = HandlerEvents(builder=builder, source=src)
    builder.connect_signals(handler)

    # load default char mapping
    handler.update_input(input_id='input_char_mapping',
                         text=src.load_char_mapping_from_file())
    handler.char_mapping_updated()

    # load default text source
    handler.update_input(input_id='input_text_src',
                         text=src.load_text_src_from_file())
    handler.text_src_updated()


    # test crypting
    # handler.update_result()

    # connect to destroy event
    main_window.connect("destroy", Gtk.main_quit)
    # start GTK main
    Gtk.main()
    
