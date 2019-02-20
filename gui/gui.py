#! /bin/python3

import gi
gi.require_version('Gtk', '3.0')


from gi.repository import Gtk, Gdk, Gio


SEP = ';'
END = '.'

class HandlerEvents:
    def __init__(self, builder):
        self.builder = builder
        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.result_buffer = self.builder.get_object('result_text').get_buffer()


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

    def open_char_mapping(self, *args):
        text = self.open_dlg('open char mapping')
        if text: self.update_input(input_id='input_char_mapping', text=text)


    def paste_text_src(self, widget):
        self.update_input(input_id='input_text_src',
                            text=self.clipboard.wait_for_text())

    def paste_char_mapping(self, widget):
        self.update_input(input_id='input_char_mapping',
                            text=self.clipboard.wait_for_text())


    def update_result(self, widget):
        pass

    # but_image.set_from_icon_name('gtk-yes', Gtk.IconSize.MENU)



if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file('ui.glade')
    main_window = builder.get_object('main_window')

    handler = HandlerEvents(builder)
    builder.connect_signals(handler)

    main_window.show_all()

    main_window.connect("destroy", Gtk.main_quit)


    Gtk.main()