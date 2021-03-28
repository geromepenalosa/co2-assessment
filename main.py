import os
from tkinter import *
from ctypes import windll

# Improve text quality
windll.shcore.SetProcessDpiAwareness(1)


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.widgets()

    def widgets(self):
        # Scrollbar
        y_scrollbar = Scrollbar(self)
        y_scrollbar.pack(side=RIGHT, fill=Y)

        # Text box
        text_box = Text(self,
                        font=("Consolas", 18),
                        undo=True,
                        yscrollcommand=y_scrollbar.set,
                        selectbackground="#0078d7", selectforeground="white")
        text_box.pack(expand=True, fill=BOTH)

        # Adjust scrollbar to text box
        y_scrollbar.config(command=text_box.yview)

        # Menu bar
        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)

        # Create menu cascades
        file_menu = Menu(menu_bar, tearoff=False)
        edit_menu = Menu(menu_bar, tearoff=False)
        format_menu = Menu(menu_bar, tearoff=False)
        view_menu = Menu(menu_bar, tearoff=False)
        help_menu = Menu(menu_bar, tearoff=False)

        # Add menu cascades to menu bar
        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        menu_bar.add_cascade(label="Format", menu=format_menu)
        menu_bar.add_cascade(label="View", menu=view_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        # File menu commands
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=lambda: self.new_file(text_box))
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=lambda: self.open_file(text_box))
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=lambda: self.save_file(text_box))
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S",
                              command=lambda: self.save_as_file(text_box))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Edit menu commands
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=text_box.edit_undo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", state=DISABLED,
                              command=lambda: self.master.focus_get().event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", state=DISABLED,
                              command=lambda: self.master.focus_get().event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V",
                              command=lambda: self.master.focus_get().event_generate("<<Paste>>"))
        edit_menu.add_command(label="Delete", accelerator="Del", state=DISABLED,
                              command=lambda: self.master.focus_get().event_generate("<<Clear>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find...", accelerator="Ctrl+F", state=DISABLED,
                              command=lambda: self.find_text(text_box))
        edit_menu.add_command(label="Replace...", accelerator="Ctrl+H", command=lambda: self.replace_text(text_box))
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A",
                              command=lambda: self.master.focus_get().event_generate("<<SelectAll>>"))
        edit_menu.add_command(label="Time/Date", accelerator="F5", command=lambda: self.show_datetime(text_box))

        # Format menu commands
        word_wrap = BooleanVar()
        format_menu.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0, variable=word_wrap,
                                    command=lambda: self.toggle_wrap(text_box, word_wrap))
        format_menu.add_command(label="Font...", command=lambda: self.edit_font(text_box))

        self.pack(expand=True, fill=BOTH)

        # View menu commands
        view_menu.add_command(label="Zoom In", accelerator="Ctrl+Plus", command=lambda: self.zoom_in(text_box))
        view_menu.add_command(label="Zoom Out", accelerator="Ctrl+Minus", command=lambda: self.zoom_out(text_box))
        view_menu.add_command(label="Restore Default Zoom", accelerator="Ctrl+0",
                                command=lambda: self.restore_zoom(text_box))
        status_bar_shown = BooleanVar()
        view_menu.add_checkbutton(label="Status Bar", onvalue=1, offvalue=0, variable=status_bar_shown,
                                  command=self.toggle_status_bar)

        # Help commands
        help_menu.add_command(label="About Clonepad")

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

    def edit_font(self, text_box):
        pass

    def zoom_in(self, text_box):
        pass

    def zoom_out(self, text_box):
        pass

    def restore_zoom(self, text_box):
        pass

    def toggle_status_bar(self):
        pass


if __name__ == "__main__":
    root = Tk()
    root.geometry("700x600")
    main_frame = MainFrame(root)
    root.mainloop()
