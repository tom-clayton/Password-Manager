#!/usr/bin/env python3

"""
ui.py

Graphical User Interface.
"""

from tkinter import Tk, StringVar, messagebox

from passwordmanager.timeout import Timeout
from passwordmanager.controller import MainController
from passwordmanager.strings import *
from passwordmanager.main_window import MainWindow
from passwordmanager.dialogues import *

TIMEOUT_RES = 100

class GUI(object):
    """The graphical user interface for the app."""
    def __init__(self):
        self.root = Tk()
        self.controller = MainController()
        self.master = StringVar()
        self.master.trace('w', self.on_keypress)
        self.main_window = MainWindow(self.root, self.master, self.on_command)
        self.handles = None
        self.current_dialogue = None
        self.timeout_state = 0
        self.monitor_timeout()
        self.main_window.disable_all_buttons()
        self.main_window.set_statusbar(READY)
        if not self.controller.db_exists:
            MasterEntryDialogue(self.root, self.change_master)

    def monitor_timeout(self):
        """Monitor timeout for change to zero"""
        new_state = self.controller.timeout.timer
        if not new_state and new_state != self.timeout_state:
            self.on_timeout()
        self.timeout_state = new_state
        self.root.after(TIMEOUT_RES, self.monitor_timeout)

    def on_timeout(self):
        """Destroy current dialogue and empty all fields."""
        if self.current_dialogue:
            self.main_window.set_statusbar(
                self.current_dialogue.on_timeout()
            )
            self.current_dialogue = None # check for memory leak

        self.master.set("")
        self.handles = None
        self.main_window.fill_box([])
        self.main_window.disable_all_buttons()

    def on_keypress(self, *args):
        """trigger/re-trigger timeout."""
        self.controller.timeout.trigger()

    def _new_dialogue(self, dialogue):
        """Create a new dialogue and wait for it to finish."""
        self.main_window.disable_all_buttons()
        self.current_dialogue = dialogue
        self.root.wait_window(dialogue.window)
        self.current_dialogue = None
        self.show_handles()

    def show_handles(self):
        """Fill handle box. Enable relevant buttons"""
        self.main_window.disable_all_buttons()
        if self.handles is not None:
            self.main_window.fill_box(self.handles)
            self.main_window.enable_non_selection_buttons()
            if self.handles:
                self.main_window.enable_selection_buttons()
                
    def on_command(self, command):
        """Call releveant method for command."""
        try:
            handle = self.handles[self.main_window.box.curselection()[0]]
        except IndexError:
            pass
        
        self.controller.timeout.trigger()

        if command == 'MAS':
            self.on_master_entry(self.master.get())
        if command == 'GET' and handle:
            self.on_get(handle)
        if command == 'SHOW' and handle:
            self.on_show(handle)
        if command == 'RENEW' and handle:
            self.on_new(handle)
        if command == 'NEW':
            self.on_new(None)
        if command == 'DEL' and handle:
            self.on_delete(handle)   
        if command == 'CHG':
            self.on_change()

        self.show_handles()

    def on_master_entry(self, master):
        """Check password correct and recive handles."""
        self.handles = self.controller.list(master)
        if self.handles is not None:
            self.main_window.set_statusbar(ENTER_SUCCESS)
        else:
            self.main_window.set_statusbar(ENTER_FAIL)

    def on_get(self, handle):
        """Get chosen password, recieve updated list of handles."""
        self.handles = self.controller.get(handle, self.master.get())
        if self.handles is not None:
            self.main_window.set_statusbar(COPY_SUCCESS)
        else:
            self.main_window.set_statusbar(ENTER_FAIL) 

    def on_show(self, handle):
        """Display 'password display' dialog window."""
        self._new_dialogue(PasswordDisplayDialogue(
                                    self.root,
                                    self.controller.get_chars,
                                    handle,
                                    self.master.get()
                                )
                           )

    def on_new(self, handle):
        """Display handle creator dialogue for given handle"""
        self._new_dialogue(PasswordCreatorDialogue(
                                self.root,
                                self.on_options,
                                handle,
                                self.handles,
                            )
                        )

    def on_options(self, handle, options):
        """Send options to password creator"""
        self.handles = self.controller.create(
                                            handle,
                                            options,
                                            self.master.get()
                                        )
        
        if self.handles is not None:
            self.show_handles()
            self.main_window.set_statusbar(CREATE_SUCCESS)
        else:
            self.main_window.set_statusbar(CREATE_FAIL)

    def on_delete(self, handle):
        """Display delete dialogue."""
        self._new_dialogue(ConfirmDialogue(
                                        self.root,
                                        DELETE_CONFIRM,
                                        DELETE_FAIL,
                                        self.delete_password,
                                        handle
                                    )
                                )
        
    def delete_password(self, handle):
        """Delete password."""
        self.handles = self.controller.delete(handle, self.master.get())
        if self.handles is not None:
            self.show_handles()
            self.main_window.set_statusbar(DELETE_SUCCESS)
        else:
            self.main_window.set_statusbar(DELETE_FAIL)
    
    def on_change(self):
        """Display master entry dialogue"""
        self._new_dialogue(MasterEntryDialogue(self.root, self.change_master))
        
    def change_master(self, new_master):
        """Change the master password."""
        result = self.controller.change_master(
                                            new_master,
                                            self.master.get()
                                        )
        if result:
            self.master.set(new_master)
            self.on_master_entry(new_master)
            self.main_window.set_statusbar(CHANGE_SUCCESS)
        else:
            self.main_window.set_statusbar(CHANGE_FAIL)
 
def main():
    ui = GUI()
    ui.root.mainloop()
    
if __name__ == "__main__":
    main()
