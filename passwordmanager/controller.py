#!/usr/bin/env python3

"""
controller.py

Main controller class and classes for contolling the ui windows.
"""

from passwordmanager.database import Database, PasswordError
from passwordmanager.password_creator import PasswordCreator
from passwordmanager.filename import FILENAME
from passwordmanager.timeout import Timeout
from passwordmanager.filename import FILENAME

import sys
import getpass
import pyperclip

TIMEOUT = 20 # in seconds 

class MainController(object):
    """Program controller"""
    def __init__(self):
        self.db = Database(FILENAME)
        self.password_creator = PasswordCreator()
        self.timeout = Timeout(TIMEOUT, self.empty_clipboard)
        self.password_on_clipboard = False

    @property
    def db_exists(self):
        """Return whether db exists."""
        return self.db.db_exists

    def list(self, master):
        """Return list of handles."""
        try:
            handles = self._get_handles(master)
            return handles
        except PasswordError:
            return None

    def get(self, handle, master):
        """Copy password for selected handle to clipboard."""
        try:
            password = self.db.get_password(handle, master)
            self._copy_to_clipboard(password)
            handles = self._get_handles(master)
            return handles
        except PasswordError:
            return None

    def get_chars(self, handle, characters, master):
        """Return requested characters from password"""
        password = self.db.get_password(handle, master)
        indexes = []
        for c in characters:
            try:
                if 0 < int(c) <= len(password):
                    indexes.append(int(c)-1)
            except ValueError:
                pass
                
        output_string = ""
        for index in indexes:
           output_string += password[index] + " "
    
        return(output_string)
    
    def create(self, handle, options, master):
        """Create and save password for handle.
        Create new handle if it doesn't exist."""
        password = self.password_creator.create(options)
        try:
            self.db.add_handle(
                            handle,
                            password,
                            master
                        )
        
            self._copy_to_clipboard(password)
            handles = self._get_handles(master)
            return handles
        except PasswordError:
            return None
        
    def change_master(self, new_master, old_master):
        """Create new database if none exists
        or change master on current one."""
        if not self.db_exists:
            self.db.create_database(new_master)
            return True
        else:
            try:
                self.db.change_master(new_master, old_master)
                return True
            except PasswordError:
                return False
 
    def delete(self, handle, master):
        """Delete selected handle from database."""
        try:
            self.db.delete_handle(handle, master)
            handles = self._get_handles(master)
            return handles
        except PasswordError:
            return None

    def _get_handles(self, master):
        """Get and sort handles from database and display in order of
        popularity."""
        handles = self.db.get_handles(master)
        handles.sort(reverse=True)
        return(tuple(map(lambda x: x[1], handles)))

    def _copy_to_clipboard(self, password):
        """Copy pass word to clipboard."""
        pyperclip.copy(password)
        self.password_on_clipboard = True
        self.timeout.trigger()
        
    def empty_clipboard(self):
        """Copy a blank space to clipboard."""
        if self.password_on_clipboard:
            pyperclip.copy(" ")
            self.password_on_clipboard = False

def main(argv):
    controller = MainController()
    if len(argv) != 2:
        print("Usage: pman handle\nThen enter master password at prompt.\n")
    else:
        controller.get(argv[1], getpass.getpass())

if __name__ == "__main__":
    sys.exit(main(sys.argv))






    
