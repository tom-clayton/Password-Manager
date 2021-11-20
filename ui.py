
"""
ui.py

User Interface classes for all the tkinter windows.
"""

from tkinter import Listbox, Scrollbar, Frame, Entry, Button, \
                    Label, Toplevel, simpledialog, \
                    Spinbox, Checkbutton, RIGHT, LEFT, BOTTOM, \
                    BOTH, END, DISABLED, NORMAL, SUNKEN, W, X

from strings import *


class MainUI(object):
    """The main user interface for the app."""
    def __init__(self, root, controller):
        """Create the main window of the user interface.

        Arguments:
        root -- tkinter root object.
        controller -- the controlling object.
        """
        # ---- Setup: ---- #

        root.title("Password Manager")
        root.geometry("260x320+200+200")
        self.root = root        

        # ---- UI Elements: ---- #
        # Main frame:
        
        self.mainframe = Frame(root)
        self.mainframe.pack(fill=X)

        # Master password entry:

        self.master_frame = Frame(self.mainframe)
        Label(self.master_frame, text="Master password:").pack(side = LEFT)
        self.master_entry = Entry(self.master_frame,
                                  show="*",
                                  textvariable=controller.master)
        self.master_entry.bind('<Return>', controller.on_master_entry)
        self.master_entry.pack(side = RIGHT)
        self.master_frame.pack()

        # Handle selector scroll box:
        
        self.selecter_frame = Frame(self.mainframe)
        self.box = Listbox(self.selecter_frame)
        self.box.pack(side = LEFT)
        self.scrollbar = Scrollbar(self.selecter_frame)
        self.scrollbar.pack(side = RIGHT, fill = BOTH)
        self.box.config(yscrollcommand = self.scrollbar.set) 
        self.scrollbar.config(command = self.box.yview)
        self.box.bind('<Return>', controller.on_get)
        self.box.bind('<Double-Button-1>', controller.on_get)
        self.selecter_frame.pack(pady=(10))

        # Action buttons:

        first_row = Frame(self.mainframe)
        self.get_button = Button(first_row,
                                 text="Get",
                                 command=controller.on_get)
        self.get_button.pack(side=LEFT)      
        self.show_button = Button(first_row,
                                   text="Show",
                                   command=controller.on_show)
        self.show_button.pack(side=LEFT)
        self.renew_button = Button(first_row,
                                   text="Renew",
                                   command=controller.on_renew)
        self.renew_button.pack(side=LEFT)
        self.delete_button = Button(first_row,
                                    text="Delete",
                                    command=controller.on_delete)
        self.delete_button.pack(side=LEFT)
        first_row.pack()

        second_row = Frame(self.mainframe)
        self.add_button = Button(second_row,
                                 text="New",
                                 command=controller.on_new)
        self.add_button.pack(side=LEFT)
        self.change_button = Button(second_row,
                                   text="Change master",
                                   command=controller.on_change)
        self.change_button.pack(side=LEFT)
        second_row.pack()

        # Statusbar:

        self.statusbar = Label(self.mainframe,
                          text=READY,
                          bd=1,
                          relief=SUNKEN,
                          anchor=W)
        self.statusbar.pack(fill=X, pady=(10, 0))     

        # ---- Show: ---- #
        
        self.mainframe.pack(side=BOTTOM)
        self.master_entry.focus_set()

    def fill_box(self, handles):
        """Display handles in scrollbox."""
        if len(handles):
            self.box.delete(0, END)
            for handle in handles:
                self.box.insert(END, handle)
            self.box.select_set(0)
            self.enable_selection_buttons()
            self.box.focus_set()
        else:
            self.empty_box()

    def get_selection(self):
        """Return selected handle."""
        return self.box.curselection()

    def empty_box(self):
        """Empty selector box."""
        self.box.delete(0, END)

    def disable_all_buttons(self):
        """Disable all buttons."""
        self.get_button.config(state=DISABLED)
        self.show_button.config(state=DISABLED)
        self.delete_button.config(state=DISABLED)
        self.renew_button.config(state=DISABLED)
        self.add_button.config(state=DISABLED)
        self.change_button.config(state=DISABLED)  

    def enable_selection_buttons(self):
        """Enable buttons that work on a selection."""
        self.get_button.config(state=NORMAL)
        self.show_button.config(state=NORMAL)
        self.delete_button.config(state=NORMAL)
        self.renew_button.config(state=NORMAL)

    def enable_non_selection_buttons(self):
        """Enable buttons that don't need a selection."""
        self.add_button.config(state=NORMAL)
        self.change_button.config(state=NORMAL)

    def set_statusbar(self, message):
        """Write message to statusbar."""
        self.statusbar.config(text=message)

class MasterEntryDialog():
    """A user interface for creating a master password."""
    def __init__(self, root, controller):
        """Create the window.

        Arguments:
        root -- tkinter root object.
        controller -- the controlling object."""
        self.window = Toplevel(root)
        self.window.title("Master password")
        self.window.geometry("350x120+600+360")
        
        Label(self.window, text=PASSWORD_ADVICE).pack()

        self.new_frame = Frame(self.window)
        self.new_label = Label(self.new_frame, text="New password:")
        self.new_label.pack(side = LEFT)
        self.master_entry = Entry(self.new_frame,
                                  show="*",
                                  textvariable=controller.new_master)
        self.master_entry.pack(side = RIGHT)
        self.master_entry.bind('<Return>', self._on_master_entry)
        self.new_frame.pack()
        
        self.confirm_frame = Frame(self.window)
        self.confirm_label = Label(self.confirm_frame, text="Confirm:")
        self.confirm_label.pack(side = LEFT)
        self.confirm_entry = Entry(self.confirm_frame,
                                   show="*",
                                   textvariable=controller.confirm_master)
        self.confirm_entry.pack(side = RIGHT)
        self.confirm_entry.bind('<Return>', controller.on_confirm_entry)
        self.confirm_frame.pack()
        
        self.ok_button = Button(self.window,
                                 text="OK",
                                 command=controller.on_confirm_entry)
        self.ok_button.pack()
        self.master_entry.focus_set()
        self.window.grab_set()

    def _on_master_entry(self, event):
        """Give confirm entry focus."""
        self.confirm_entry.focus_set()
        
class HandleCreatorDialog():
    """A user interface to create a password with a set of constraints."""
    def __init__(self, root, handle, controller):
        """Create the window.

        Arguments:
        root -- the main app's tkinter object.
        handle -- the handle if it is a renewal.
        controller -- the controlling object.
        """         
        self.window = Toplevel(root)
        self.window.title("New password")
        self.window.geometry("350x170+600+360")

        self.handle_frame = Frame(self.window)
        if not handle:
            Label(self.handle_frame,
                  text="New password name:").pack(side = LEFT)
            self.handle_entry = Entry(self.handle_frame,
                                      textvariable=controller.new_handle)
            self.handle_entry.pack(side=RIGHT)
            self.handle = None
            self.handle_entry.focus_set()
        else:
            Label(self.handle_frame, text=f"New password for {handle}.").pack()
            self.handle = handle
        self.handle_frame.pack()

        
        Label(self.window, text="Password will contain:").pack()
        self.spin_frame = Frame(self.window)
        Spinbox(self.spin_frame, from_=8, to=16,
                textvariable=controller.length_option).pack(side=LEFT)
        Label(self.spin_frame, text="characters").pack(side=RIGHT)
        self.spin_frame.pack()
        
        self.options_frame = Frame(self.window)
        Checkbutton(self.options_frame,
                    text="Upper case",
                    variable=controller.upper_option).pack(anchor=W)
        Checkbutton(self.options_frame,
                    text="Digits",
                    variable=controller.digits_option).pack(anchor=W)
        Checkbutton(self.options_frame,
                    text="Special characters",
                    variable=controller.special_option).pack(anchor=W)
        self.options_frame.pack()
        self.create_button = Button(self.window,
                                text="Create",
                                command=controller.on_create)
        self.create_button.pack()
        self.window.grab_set()

class PasswordDisplayDialog():
    """A user interface to display parts or all of a password."""
    def __init__(self, root, controller):
        """Create the window.

        Arguments:
        root -- the main app's tkinter object.
        controller -- the controlling object.
        """
        self.window = Toplevel(root)
        self.window.title("Show password")
        self.window.geometry("350x120+600+360")
        
        Label(self.window, text=SHOW_REQUEST).pack()
        self.entry = Entry(self.window, textvariable=controller.input)
        self.entry.bind("<Return>", controller.on_confirm)
        self.entry.pack()
        self.button = Button(self.window,
                             text="Show",
                             command=controller.on_confirm)
        self.button.pack()
        self.label = Label(self.window, textvariable=controller.output)
        self.label.pack()
