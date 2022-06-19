#!/usr/bin/env python3

"""
controller.py

Main controller class and classes for contolling the ui windows.
"""

from passwordmanager.database import Database, PasswordError
from passwordmanager.ui import (
                            MainUI, 
                            MasterEntryDialog, 
                            HandleCreatorDialog,
                            PasswordDisplayDialog,
                        )
from passwordmanager.timeout import Timeout
from passwordmanager.password_creator import PasswordCreator
from passwordmanager.strings import *
from passwordmanager.filename import FILENAME

from tkinter import Tk, StringVar, IntVar, messagebox
import pyperclip

from random import choice
import os

TIMEOUT = 20 # in seconds 

class MainController(object):
    """Program controller"""
    def __init__(self):
        self.db = Database(FILENAME)
        self.tk_root = Tk()
        self.timeout = Timeout(self.tk_root, TIMEOUT, self.on_timeout)
        self.master = StringVar()
        self.master.trace('w', self.on_keypress)
        self.handles = ()
        self.ui = MainUI(self.tk_root, self)
        self.opened_window = None
        self._on_init()
        self.tk_root.mainloop()
                
    def on_timeout(self):
        """Destroy open window if necessary. Empty all fields in main ui."""
        try:
            self.opened_window.on_timeout()
        except AttributeError:
            pass
        self.master.set("")
        self.ui.empty_box()
        self.ui.disable_all_buttons()
        self._empty_clipboard()
        self.ui.set_statusbar(READY)
        
    def on_keypress(self, *args):
        """trigger/re-trigger timeout, unless the master password is blank."""
        if self.master.get():
            self.timeout.trigger()

    def on_master_entry(self, *args):
        """Fill handle selection box."""
        if not self.opened_window:
            try:
                self._update_handles()
                self.ui.enable_non_selection_buttons()
                self.ui.set_statusbar(ENTER_SUCCESS)
            except PasswordError:
                self.ui.set_statusbar(ENTER_FAIL)

    def on_get(self, *args):
        """Copy password for selected handle to clipboard."""
        if not self.opened_window:
            try:
                password = self.db.get_password(self._get_selected_handle(),
                                                self.master.get())
                self._copy_to_clipboard(password)
                self.timeout.trigger()
                handles = self._update_handles()
                self.ui.set_statusbar(COPY_SUCCESS)
            except PasswordError:
                self.ui.set_statusbar(ENTER_FAIL)

    def on_show(self):
        """Display 'password display' dialog window."""
        if not self.opened_window:
            self.timeout.trigger()
            password = self.db.get_password(self._get_selected_handle(),
                                        self.master.get())
            password_display = PasswordDisplay(self.tk_root, password)
            self.opened_window = password_display
            self.tk_root.wait_window(password_display.ui.window)
            self.opened_window = None

    def on_new(self):
        """Start password creator window with no handle."""
        self._create_handle(handle=None)

    def on_renew(self):
        """Start password creator window with selected handle."""
        self._create_handle(handle=self._get_selected_handle())

    def on_delete(self):
        """Delete selected handle from database, after confirmation from user."""
        if not self.opened_window:
            self.timeout.trigger()
            handle = self._get_selected_handle()
            if messagebox.askokcancel(f"Delete {handle} password",
                                          DELETE_CONFIRM):
                self.db.delete_handle(handle, self.master.get())
                self._update_handles()
                self.ui.set_statusbar(DELETE_SUCCESS)
            else:
                self.ui.set_statusbar(DELETE_FAIL)

    def on_change(self):
        """Display master change window."""
        if not self.opened_window:
            self.timeout.trigger()
                    
            master_dialog = MasterChanger(self.tk_root)
            self.opened_window = master_dialog
            self.tk_root.wait_window(master_dialog.ui.window)
            if master_dialog.confirmed_master: 
                try:
                    self.db.change_master(self.master.get(), 
                                              master_dialog.confirmed_master)
                    self.master.set(master_dialog.confirmed_master)
                    self.on_master_entry()
                    self.ui.set_statusbar(CHANGE_SUCCESS)
                except PasswordError:
                    self.ui.set_statusbar(CHANGE_FAIL)
            else:
                self.ui.set_statusbar(CHANGE_FAIL)
            

            self.opened_window = None

    def _create_handle(self, handle=None):
        """Start password creator window.
        Ask to renew if handle already exists.
        Copy password to clipboard.
        """
        if not self.opened_window:
            self.timeout.trigger()
            handle_creator = HandleCreator(self.tk_root, handle)
            self.opened_window = handle_creator
            self.tk_root.wait_window(handle_creator.ui.window)
            if handle_creator.password:
                try:
                    handle = handle or handle_creator.handle
                    if handle not in self.handles or \
                      messagebox.askokcancel(f"Renew {handle} password",
                                             OVERWRITE_CONFIRM):
                        self.db.add_handle(handle,
                                           handle_creator.password,
                                           self.master.get())
                        self._copy_to_clipboard(handle_creator.password)
                        self._update_handles()
                        self.ui.set_statusbar(CREATE_SUCCESS)
                except (PasswordError):
                    self.ui.set_statusbar(CREATE_FAIL)
            else:
                self.ui.set_statusbar(CREATE_FAIL)
                
            self.opened_window = None 
                       
    def _on_init(self):
        """Disable all buttons.
        Check for database.
        Create if necesary."""
        self.ui.disable_all_buttons()
        if not self.db.db_exists:
            master_dialog = MasterChanger(self.tk_root)
            self.tk_root.wait_window(master_dialog.ui.window)
            if master_dialog.confirmed_master:
                self.master.set(master_dialog.confirmed_master)
                self.db.create_database(self.master.get())
                self.on_master_entry()
                self.ui.set_statusbar(CREATE_DB_SUCCESS)
            else:
                self.tk_root.destroy()
                self.tk_root.quit()
        else:        
            self.ui.set_statusbar(READY)
    
    def _get_selected_handle(self):
        """Return selected handle."""
        return self.handles[self.ui.get_selection()[0]]

    def _update_handles(self):
        """Get and sort handles from database and display in order of
        popularity."""
        handles = self.db.get_handles(self.master.get())
        handles.sort(reverse=True)
        self.handles = tuple(map(lambda x: x[1], handles))
        self.ui.fill_box(self.handles)

    def _copy_to_clipboard(self, password):
        """Copy pass word to clipboard."""
        pyperclip.copy(password)
        
    def _empty_clipboard(self):
        """Copy a blank space to clipboard."""
        pyperclip.copy(" ")

       
class MasterChanger(object):
    """Controls master password change dialogue."""
    def __init__(self, tk_root):
        """Setup variables, start dialogue."""
        self.new_master = StringVar()
        self.confirm_master = StringVar()
        self.confirmed_master = None
        self.ui = MasterEntryDialog(tk_root, self)        

    def on_confirm_entry(self, *args):
        """Check masters are the same, destroy the window."""
        new_master = self.new_master.get()
        confirm_master = self.confirm_master.get()
        if new_master and new_master == confirm_master:
            self.confirmed_master = new_master
            self.ui.window.destroy()

    def on_timeout(self):
        """Destroy the window"""
        self.ui.window.destroy()
        
class HandleCreator(object):
    """Controls handle creator dialogue."""
    def __init__(self, tk_root, handle):
        """Setup variables, start dialogue."""
        self.handle = handle
        self.password = None
        self.new_handle = StringVar()
        self.length_option = IntVar(value=16)
        self.upper_option = IntVar(value=1)
        self.digits_option = IntVar(value=1)
        self.special_option = IntVar(value=1)
        self.ui = HandleCreatorDialog(tk_root, handle, self)

    def create_password(self):
        """Create a password with the password creator."""
        creator = PasswordCreator()
        self.password = creator.create(self.length_option.get(),
                                       self.upper_option.get(),
                                       self.digits_option.get(),
                                       self.special_option.get())
        

    def on_create(self):
        """Create the password.""" 
           
        self.handle = self.handle or self.new_handle.get()
        print("on_create: handle:", self.handle) 
        if self.handle:
            self.create_password()
            self.ui.window.destroy()

    def on_timeout(self):
        """Destroy the window"""
        self.ui.window.destroy()
   
class PasswordDisplay(object):
    """Controls password display dialogue."""
    def __init__(self, tk_root, password):
        """Setup variables, start dialogue."""
        self.password = password
        self.input = StringVar()
        self.output = StringVar()
        self.ui = PasswordDisplayDialog(tk_root, self)

    def on_confirm(self, *args):
        """Display selected characters from password."""
        characters = self.input.get().split()
        if not characters:
            indexes = [i for i in range(len(self.password))]
        else:
            indexes = []
            for c in characters:
                try:
                    if 0 < int(c) <= len(self.password):
                        indexes.append(int(c)-1)
                except ValueError:
                    pass
                
        output_string = ""
        for index in indexes:
           output_string += self.password[index] + " "
    
        self.output.set(output_string)

    def on_timeout(self):
        """Destroy the window"""
        self.ui.window.destroy()

def main():
    controller = MainController()

if __name__ == "__main__":
    main()
    
