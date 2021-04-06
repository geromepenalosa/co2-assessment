import os
from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import filedialog

# Improve text quality. NOTE: This block of code is ignored on macOS.
if os.name == 'nt':
     from ctypes import windll
     windll.shcore.SetProcessDpiAwareness(1)

global opened_file
opened_file = False


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        # Initialize variables
        self.y_scrollbar, self.text_box, self.menu_bar, self.status_bar, \
            self.file_menu, self.edit_menu, self.format_menu, self.view_menu, \
            self.var_wordwrap, self.var_status_bar_shown = [None] * 10
        self.font_size = 11
        self.zoom_scale = 1
        self.zoom_count = 100
        self.widgets()

    def widgets(self):
        # Scrollbar
        self.y_scrollbar = Scrollbar(self)
        self.y_scrollbar.pack(side=RIGHT, fill=Y)

        # Text box
        self.text_box = Text(self,
                             font=("Consolas", self.font_size),
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

        # Add menu cascades to menu bar
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # File menu commands
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=lambda: self.new_file(None))
        self.file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=lambda: self.open_file(None))
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=lambda: self.save_file(None))
        self.file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S",
                                   command=lambda: self.save_as_file(None))
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
                                   command=lambda: self.find_text(None))
        self.edit_menu.add_command(label="Replace...", accelerator="Ctrl+H",
                                   command=lambda: self.replace_text(None))
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", accelerator="Ctrl+A",
                                   command=lambda: self.master.focus_get().event_generate("<<SelectAll>>"))
        self.edit_menu.add_command(label="Time/Date", accelerator="F5",
                                   command=lambda: self.show_datetime(None))

        # Format menu commands
        self.var_wordwrap = BooleanVar()
        self.format_menu.add_checkbutton(label="Word Wrap", onvalue=1, offvalue=0, variable=self.var_wordwrap,
                                         command=lambda: self.toggle_wrap)
        self.format_menu.add_command(label="Font...", command=lambda: FontWindow(root, self))

        self.pack(expand=True, fill=BOTH)

        # View menu commands
        self.view_menu.add_command(label="Zoom In", accelerator="Ctrl+Equal",
                                   command=lambda: self.zoom_in(None))
        self.view_menu.add_command(label="Zoom Out", accelerator="Ctrl+Minus",
                                   command=lambda: self.zoom_out(None))
        self.view_menu.add_command(label="Restore Default Zoom", accelerator="Ctrl+0",
                                   command=lambda: self.restore_zoom(None))
        self.var_status_bar_shown = BooleanVar()
        self.var_status_bar_shown.set(True)
        self.view_menu.add_checkbutton(label="Status Bar", onvalue=True, offvalue=False,
                                       variable=self.var_status_bar_shown,
                                       command=self.toggle_status_bar)

        # Zoom bindings
        self.text_box.bind("<Control-MouseWheel>", self.mouse_wheel)
        self.text_box.bind("<Control-equal>", self.zoom_in)
        self.text_box.bind("<Control-minus>", self.zoom_out)
        self.text_box.bind("<Control-0>", self.restore_zoom)

        # Status bar
        self.status_bar = StatusBar(self.text_box)
        self.text_box.bind('<<Modified>>', self.status_bar.check)

    def new_file(self, event):
        self.text_box.delete("1.0",END)
        root.title("New file - Notepad")

        global opened_file
        opened_file = False
        
    def open_file(self, event):
        self.text_box.delete("1.0",END)
        text_file = filedialog.askopenfilename(initialdir="", title="Open File",
                    filetypes=(("Text files", "*.txt"),("HTML Files","*.html"),("Python files","*.py"),("All files","*.*")))
                    
        # Checks for filename existence
        if text_file:
            # To access file for later use
            global opened_file
            opened_file = text_file

        # Update menu bar
        filename = text_file
        root.title("{} - Notepad".format(filename))

        # Read file contents
        text_file = open(text_file,"r")
        read_text = text_file.read()
        self.text_box.insert(END, read_text)

        #Close open file selection menu
        text_file.close()

    def save_as_file(self, event):
        text_file = filedialog.asksaveasfilename(defaultextension=".*",initialdir= "", title="Save file as",
                    filetypes=(("Text files", "*.txt"),("HTML Files","*.html"),("Python files","*.py"),("All files","*.*")))
        if text_file:
            # Update menu bar
            filename = text_file
            root.title("{} - Notepad (Saved)".format(filename))

            # File saving
            text_file = open(text_file, "w")
            text_file.write(self.text_box.get(1.0,END))

            #Close file
            text_file.close()
    
    def save_file(self, event):
        global opened_file
        # File saving
        text_file = open(opened_file, "w")
        text_file.write(self.text_box.get(1.0,END))
        #Close file
        text_file.close()
        if opened_file == False:
            text_file = filedialog.asksaveasfilename(defaultextension=".*",initialdir= "", title="Save file as",
                    filetypes=(("Text files", "*.txt"),("HTML Files","*.html"),("Python files","*.py"),("All files","*.*")))
            if text_file:
                filename = text_file
                root.title("{} - Notepad (Saved)".format(filename))
                text_file = open(text_file, "w")
                text_file.write(self.text_box.get(1.0,END))
                text_file.close()

    def find_text(self, event):
        pass

    def replace_text(self, event):
        pass

    def show_datetime(self, event):
        pass

    def toggle_wrap(self):
        pass

    def mouse_wheel(self, event):
        if event.delta == -120:
            self.zoom_out(event)
        if event.delta == 120:
            self.zoom_in(event)

    def zoom_in(self, event):
        textbox_font_and_size = self.text_box['font']
        current_font = textbox_font_and_size.rsplit(' ', 1)[0].replace('{', '').replace('}', '')
        if self.zoom_count < 500:  # 500% is the maximum percentage to zoom-in
            self.zoom_scale += 1
            self.zoom_count += 10
            font_size = self.font_size + self.zoom_scale
            self.text_box.config(font=(current_font, font_size))
        self.status_bar.lbl_zoom_count.config(text=f'{self.zoom_count}%')

    def zoom_out(self, event):
        textbox_font = self.text_box['font']
        current_font = textbox_font.rsplit(' ', 1)[0].replace('{', '').replace('}', '')
        if self.zoom_count >= 20:  # 10% is the minimum zoom_count
            self.zoom_scale -= 1
            self.zoom_count -= 10
            font_size = self.font_size + self.zoom_scale
            self.text_box.config(font=(current_font, font_size))
        self.status_bar.lbl_zoom_count.config(text=f'{self.zoom_count}%')

    def restore_zoom(self, event):
        textbox_font = self.text_box['font']
        current_font = textbox_font.rsplit(' ', 1)[0].replace('{', '').replace('}', '')
        self.zoom_scale = 1
        self.zoom_count = 100
        self.text_box.config(font=(current_font, self.font_size))
        self.status_bar.lbl_zoom_count.config(text=f'{self.zoom_count}%')

    def toggle_status_bar(self):
        if self.var_status_bar_shown:
            self.status_bar.pack_forget()
            self.var_status_bar_shown = False
        else:
            self.status_bar.pack(side=BOTTOM, fill='x')
            self.var_status_bar_shown = True


class FontWindow(Toplevel):
    def __init__(self, master, main_frame):
        super().__init__(master)
        self.mainframe = main_frame
        # Adjust window
        self.title('Font')
        self.geometry('320x320')
        self.resizable(False, False)
        # Initialize variables
        self.lbl_font, self.lbl_size, self.lbl_sample, \
        self.cbx_font, self.cbx_size, \
        self.btn_confirm, self.btn_cancel, \
        self.textbox_font, self.textbox_size, \
        self.canvas_sample, \
        self.text_sample = [None] * 11
        self.widgets()

    def widgets(self):
        # Font currently used in text box
        textbox_font_and_size = self.mainframe.text_box['font']
        self.textbox_font = textbox_font_and_size.rsplit(' ', 1)[0].replace('{', '').replace('}', '')
        self.textbox_size = str(self.mainframe.font_size)

        # Font label
        self.lbl_font = Label(self, text="Font:")
        self.lbl_font.place(x=10, y=10)

        # Font combobox
        font_families = font.families()
        self.cbx_font = ttk.Combobox(self, width=22)
        self.cbx_font['values'] = font_families
        self.cbx_font.current(self.cbx_font['values'].index(self.textbox_font))
        self.cbx_font.bind('<<ComboboxSelected>>', self.update_sample)
        self.cbx_font.place(x=10, y=35)

        # Font size label
        self.lbl_size = Label(self, text="Size:")
        self.lbl_size.place(x=230, y=10)

        # Font size combobox
        self.cbx_size = ttk.Combobox(self, width=6)
        self.cbx_size['values'] = tuple(range(8, 73, 1))
        self.cbx_size.current(self.cbx_size['values'].index(self.textbox_size))
        self.cbx_size.bind('<<ComboboxSelected>>', self.update_sample)
        self.cbx_size.place(x=230, y=35)

        # Sample canvas
        self.canvas_sample = Canvas(self, width=250, height=100, highlightbackground="#cdcdcd", highlightthickness=1)
        self.canvas_sample.place(x=10, y=100)
        self.text_sample = self.canvas_sample.create_text(125, 50, anchor=CENTER, text='AaBbYyZz',
                                                          font=(self.cbx_font.get(), self.cbx_size.get()))

        # Sample label
        self.lbl_sample = Label(self, text="Sample")
        self.lbl_sample.place(x=15, y=85)

        # OK button
        self.btn_confirm = Button(self, text="OK", width=10, command=self.exit)
        self.btn_confirm.place(x=115, y=275)

        # Cancel button
        self.btn_cancel = Button(self, text="Cancel", width=10, command=self.destroy)
        self.btn_cancel.place(x=220, y=275)

    def update_sample(self, event):
        new_font = self.cbx_font.get() if self.cbx_font.get() else self.textbox_font
        new_size = self.cbx_size.get() if self.cbx_size.get() else self.textbox_size
        self.canvas_sample.itemconfigure(self.text_sample, font=(new_font, new_size))

    def exit(self):
        new_font = self.cbx_font.get() if self.cbx_font.get() else self.textbox_font
        new_size = self.cbx_size.get() if self.cbx_size.get() else self.textbox_size
        self.mainframe.text_box.config(font=(new_font, int(new_size) + self.mainframe.zoom_scale))
        self.mainframe.font_size = int(new_size)
        self.destroy()


class StatusBar(Frame):
    def __init__(self, master):
        super().__init__(master)
        # Initialize variables
        self.lbl_word_count, self.lbl_char_count, self.lbl_zoom_count = [None] * 3
        self.widgets()
        self.pack(side=BOTTOM, fill=X)

    def widgets(self):
        self.lbl_word_count = Label(self, text='Words: 0 ')
        self.lbl_word_count.grid(row=0, column=0, rowspan=2)

        self.lbl_char_count = Label(self, text='Characters: 0     |')
        self.lbl_char_count.grid(row=0, column=1, rowspan=2)

        self.lbl_zoom_count = Label(self, text='100%')
        self.lbl_zoom_count.grid(row=0, column=2, rowspan=2)

    def check(self, event):
        if self.master.edit_modified():
            word_count = len(self.master.get(1.0, 'end-1c').split())
            character_count = len(self.master.get(1.0, 'end-1c'))
            self.lbl_word_count.config(text=f'Words: {word_count} ')
            self.lbl_char_count.config(text=f'Characters: {character_count}     |')
        self.master.edit_modified(False)


if __name__ == "__main__":
    root = Tk()
    root.title("Notepad")
    root.geometry("700x600")
    mainframe = MainFrame(root)
    root.mainloop()
