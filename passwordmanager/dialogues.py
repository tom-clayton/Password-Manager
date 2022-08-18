
from tkinter import Frame, Entry, Label, Button, Toplevel, Spinbox, IntVar, \
                    Checkbutton, StringVar, LEFT, RIGHT, W, messagebox

from strings import *

class PasswordDisplayDialogue():
    """A user interface to display parts or all of a password."""
    def __init__(self, root, request_chars, handle, master):
        """Create the window.

        Arguments:
        root -- tkinter root object.
        request_chars -- function to request password characters.
        handle -- handle for password.
        master -- master password
        """
        self.request_chars = request_chars
        self.handle = handle
        self.master = master

        self.input = StringVar()
        self.output = StringVar()
        
        self.window = Toplevel(root)
        self.window.title("Show password")
        self.window.geometry("350x120+600+360")
        
        Label(self.window, text=SHOW_REQUEST).pack()
        self.entry = Entry(self.window, textvariable=self.input)
        self.entry.bind("<Return>", self.on_confirm)
        self.entry.pack()
        self.button = Button(self.window,
                             text="Show",
                             command=self.on_confirm)
        self.button.pack()
        self.label = Label(self.window, textvariable=self.output)
        self.label.pack()
        self.window.grab_set()

    def on_confirm(self, *args):
        """Get requested characters from controller."""
        if self.input.get():
            self.output.set(
                    self.request_chars(
                            self.handle,
                            self.input.get().split(),
                            self.master
                        )
                    )
    def on_timeout(self):
        """Destroy window."""
        self.window.destroy()
        return None
                            
class MasterEntryDialogue():
    """A user interface for creating a master password."""
    def __init__(self, root, change_master):
        """Create the window.

        Arguments:
        root -- tkinter root object.
        change_master -- function to change master password.
        """

        self.change_master = change_master

        self.new_master = StringVar()
        self.confirmed_master = StringVar()
        
        self.window = Toplevel(root)
        self.window.title("Master password")
        self.window.geometry("350x120+600+360")

        Label(self.window, text=PASSWORD_ADVICE).pack()

        self.new_frame = Frame(self.window)
        self.new_label = Label(self.new_frame, text="New password:")
        self.new_label.pack(side = LEFT)
        self.master_entry = Entry(self.new_frame,
                                  show="*",
                                  textvariable=self.new_master)
        self.master_entry.pack(side = RIGHT)
        self.master_entry.bind('<Return>', self.on_master_entry)
        self.new_frame.pack()
        
        self.confirm_frame = Frame(self.window)
        self.confirm_label = Label(self.confirm_frame, text="Confirm:")
        self.confirm_label.pack(side = LEFT)
        self.confirm_entry = Entry(self.confirm_frame,
                                   show="*",
                                   textvariable=self.confirmed_master)
        self.confirm_entry.pack(side = RIGHT)
        self.confirm_entry.bind('<Return>', self.on_confirm_entry)
        self.confirm_frame.pack()
        
        self.ok_button = Button(self.window,
                                 text="OK",
                                 command=self.on_confirm_entry)
        self.ok_button.pack()
        self.master_entry.focus_set()
        self.window.grab_set()

    def on_master_entry(self, *args):
        """Give confirm entry focus."""
        self.confirm_entry.focus_set()

    def on_confirm_entry(self, *args):
        """Send master to controller object."""
        if self.new_master.get() == self.confirmed_master.get():
            self.change_master(self.new_master.get())
            self.window.destroy()

    def on_timeout(self):
        """Destroy window."""
        self.window.destroy()
        return CHANGE_FAIL
        
class PasswordCreatorDialogue():
    """A user interface to create a password with a set of constraints."""
    def __init__(
                self,
                root,
                create_password,
                handle,
                handles,
            ):
        """Create the window.

        Arguments:
        root -- tkinter root object.
        create_password -- function to create password.
        handle -- handle for password.
        handles -- list of handles.
        master -- master password.
        """
        self.root = root
        self.create_password = create_password
        self.handles = handles

        self.new_handle = StringVar()
        self.length_option = IntVar(value=16)
        self.upper_option = IntVar(value=1)
        self.digits_option = IntVar(value=1)
        self.special_option = IntVar(value=1)
        self.popup = None
        
        self.window = Toplevel(root)
        self.window.title("New password")
        self.window.geometry("350x170+600+360")

        self.handle_frame = Frame(self.window)
        if not handle:
            Label(self.handle_frame,
                  text="New password name:").pack(side = LEFT)
            self.handle_entry = Entry(self.handle_frame,
                                      textvariable=self.new_handle)
            self.handle_entry.pack(side=RIGHT)
            self.handle = None
            self.handle_entry.focus_set()
        else:
            Label(self.handle_frame, text=f"New password for {handle}.").pack()
            self.new_handle.set(handle)
        self.handle_frame.pack()

        
        Label(self.window, text="Password will contain:").pack()
        self.spin_frame = Frame(self.window)
        Spinbox(self.spin_frame, from_=8, to=16,
                textvariable=self.length_option).pack(side=LEFT)
        Label(self.spin_frame, text="characters").pack(side=RIGHT)
        self.spin_frame.pack()
        
        self.options_frame = Frame(self.window)
        Checkbutton(self.options_frame,
                    text="Upper case",
                    variable=self.upper_option).pack(anchor=W)
        Checkbutton(self.options_frame,
                    text="Digits",
                    variable=self.digits_option).pack(anchor=W)
        Checkbutton(self.options_frame,
                    text="Special characters",
                    variable=self.special_option).pack(anchor=W)
        self.options_frame.pack()
        self.create_button = Button(self.window,
                                text="Create",
                                command=self.on_create)
        self.create_button.pack()
        self.create_button.focus_set()
        self.window.grab_set()

    def on_create(self, *args):
        """Display overwrite dialogue if required."""
        new_handle = self.new_handle.get()
        if new_handle:
            if new_handle in self.handles:
                self.popup = ConfirmDialogue(
                            self.root,
                            OVERWRITE_CONFIRM,
                            CREATE_FAIL,
                            self.on_confirm,
                            new_handle,
                        ) 
            else:
                self.on_confirm(new_handle)
            

    def on_confirm(self, handle):
        """Create a password for handle"""
        options = [
            self.length_option.get(),
            self.upper_option.get(),
            self.digits_option.get(),
            self.special_option.get()
        ]
        self.create_password(handle, options)
        self.window.destroy()

    def on_timeout(self):
        """Destroy window."""
        if self.popup:
            self.popup.window.destroy()
        self.window.destroy()
        return CREATE_FAIL

class ConfirmDialogue():
    """A user interface to display parts or all of a password."""
    def __init__(self, root, message, fail_message, confirm, handle):
        """Create the window.

        Arguments:
        root -- tkinter root object.
        request_chars -- function to delete password.
        handle -- handle for password.
        master -- master password
        """
        self.confirm = confirm
        self.fail_message = fail_message
        self.handle = handle
        
        self.window = Toplevel(root)
        self.window.title(f"Password for {handle}")
        self.window.geometry("360x80+600+360")

        Label(self.window, text=message).pack()

        button_frame = Frame(self.window)
        ok_button = Button(button_frame, text="OK", command=self.on_ok)
        ok_button.pack(side=LEFT)

        cancel_button = Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side = LEFT)
        button_frame.pack()
        
        cancel_button.focus_set()
        self.window.grab_set()

    def on_ok(self, *args):
        """Call confirm."""
        self.confirm(self.handle)
        self.window.destroy()
        
    def on_cancel(self, *args):
        """Destroy window."""
        self.window.destroy()

    def on_timeout(self):
        """Destroy window."""
        self.window.destroy()
        return self.fail_message
