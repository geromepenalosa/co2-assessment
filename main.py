import os
from ctypes import windll
from tkinter import *
from tkinter import font
from tkinter import ttk

# Improve text quality
windll.shcore.SetProcessDpiAwareness(1)


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        # Initialize variables
        self.y_scrollbar, self.text_box, self.menu_bar, \
            self.file_menu, self.edit_menu, self.format_menu, self.view_menu, self.help_menu, \
            self.var_wordwrap, self.var_status_bar_shown = [None] * 10
        self.widgets()

    def widgets(self):
        # Scrollbar
        self.y_scrollbar = Scrollbar(self)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)

        # Text box
        self.text_box = Text(self,
                             font=("Consolas", 11),
                             undo=True,
                             yscrollcommand=self.y_scrollbar.set,
                             selectbackground="#0078d7", selectforeground="white")
        self.text_box.pack(expand=True, fill=BOTH)

        # Adjust scrollbar to text box
        self.y_scrollbar.config(command=self.text_box.yview)

        # Menu bar
        self.menu_bar = Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # Create menu cascades
        self.file_menu = Menu(self.menu_bar, tearoff=False)
        self.edit_menu = Menu(self.menu_bar, tearoff=False)
        self.format_menu = Menu(self.menu_bar, tearoff=False)
        self.view_menu = Menu(self.menu_bar, tearoff=False)
        self.help_menu = Menu(self.menu_bar, tearoff=False)

        # Add menu cascades to menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        # File menu commands
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=lambda: self.new_file(self.text_box))
        self.file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=lambda: self.open_file(self.text_box))
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=lambda: self.save_file(self.text_box))
        self.file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S",
                                   command=lambda: self.save_as_file(self.text_box))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

        # Edit menu commands
        self.edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.text_box.edit_undo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator="Ctrl+X", state=DISABLED,
                                   command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", accelerator="Ctrl+C", state=DISABLED,
                                   command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", accelerator="Ctrl+V",
                                   command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        self.edit_menu.add_command(label="Delete", accelerator="Del", state=DISABLED,
                                   command=lambda: self.master.focus_get().event_generate("<<Clear>>"))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find...", accelerator="Ctrl+F", state=DISABLED,
                                   command=lambda: self.find_text(self.text_box))
        self.edit_menu.add_command(label="Replace...", accelerator="Ctrl+H",
                                   command=lambda: self.replace_text(self.text_box))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", accelerator="Ctrl+A",
                                   command=lambda: self.master.focus_get().event_generate("<<SelectAll>>"))
        self.edit_menu.add_command(label="Time/Date", accelerator="F5",
                                   command=lambda: self.show_datetime(self.text_box))

        # Format menu commands
        self.var_wordwrap = BooleanVar()
        self.format_menu.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0, variable=self.var_wordwrap,
                                         command=lambda: self.toggle_wrap(self.text_box, self.var_wordwrap))
        self.format_menu.add_command(label="Font...", command=lambda: FontWindow(root, self))

        self.pack(expand=True, fill=BOTH)

        # View menu commands
        self.view_menu.add_command(label="Zoom In", accelerator="Ctrl+Plus",
                                   command=lambda: self.zoom_in(self.text_box))
        self.view_menu.add_command(label="Zoom Out", accelerator="Ctrl+Minus",
                                   command=lambda: self.zoom_out(self.text_box))
        self.view_menu.add_command(label="Restore Default Zoom", accelerator="Ctrl+0",
                                   command=lambda: self.restore_zoom(self.text_box))
        self.var_status_bar_shown = BooleanVar()
        self.view_menu.add_checkbutton(label="Status Bar", onvalue=1, offvalue=0, variable=self.var_status_bar_shown,
                                       command=self.toggle_status_bar)

        # Help commands
        self.help_menu.add_command(label="About Clonepad")

    def new_file(self, text_box):
        pass

    def open_file(self, text_box):
        pass

    def save_file(self, text_box):
        pass

    def save_as_file(self, text_box):
        pass

    def find_text(self, text_box):
        pass

    def replace_text(self, text_box):
        pass

    def show_datetime(self, text_box):
        pass

    def toggle_wrap(self, text_box, word_wrap):
        pass

    def zoom_in(self, text_box):
        pass

    def zoom_out(self, text_box):
        pass

    def restore_zoom(self, text_box):
        pass

    def toggle_status_bar(self):
        pass


class FontWindow(Toplevel):
    def __init__(self, master, main_frame):
        super().__init__(master)
        self.mainframe = main_frame
        # Adjust window
        self.title('Font')
        self.geometry('480x480')
        self.resizable(False, False)
        # Initialize variables
        self.lbl_font, self.lbl_font_size, \
            self.cbx_font, self.cbx_font_size, \
            self.btn_confirm, self.btn_cancel = [None] * 6
        self.widgets()

    def widgets(self):
        # Font window labelling
        self.lbl_font = Label(self, text="Font:{0}".format(" " * 35))
        self.lbl_font_size = Label(self, text="Font Size:{0}".format(" " * 15))
        self.lbl_font.grid(row=0, column=0, padx=5, columnspan=2)
        self.lbl_font_size.grid(row=0, column=3, padx=5, columnspan=2)

        # List font families
        font_families = font.families()
        self.cbx_font = ttk.Combobox(self, width=20)
        self.cbx_font['values'] = font_families
        self.cbx_font.grid(row=1, column=0, padx=5, columnspan=2)

        # List font sizes
        self.cbx_font_size = ttk.Combobox(self, width=14)
        self.cbx_font_size['values'] = tuple(range(8, 72, 1))
        self.cbx_font_size.grid(row=1, column=3, padx=5, columnspan=2)

        # Button
        self.btn_confirm = Button(self, text="Ok", command=self.exit)
        self.btn_confirm.grid(row=4, column=9)

        self.btn_cancel = Button(self, text="Cancel", command=self.destroy)
        self.btn_cancel.grid(row=4, column=10)

    def exit(self):
        self.mainframe.text_box.config(font=(self.cbx_font.get(), self.cbx_font_size.get()))
        self.destroy()


if __name__ == "__main__":
    root = Tk()
    root.geometry("700x600")
    mainframe = MainFrame(root)
    root.mainloop()
