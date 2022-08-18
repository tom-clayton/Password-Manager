
"""
database.py

class for controlling the encrypted database of passwords.
"""

import os
import json
from passwordmanager.securestrings import save_string, load_string
from threading import Lock

class Database(object):
    """Secure password database manager."""
    def __init__(self, filename):
        """check data file exists"""
        self.filename = filename
        self.db_exists = os.path.isfile(self.filename)
        self.mutex = Lock()

    def create_database(self, master):
        """Create new database.

        Arguments:
        master - the master password."""
        self.save({}, master)

    def save(self, data, master):
        """save dictionary to file.

        Arguments:
        data - the dictionary with all the data.
        master - the master password."""
        save_string(self.filename, master, json.dumps(data))
            
    def load(self, master):
        """load dictionary from file.

        Arguments:
        master - the master password.
        Returns:
        the dictionary with all the data."""
        try:
            return json.loads(load_string(self.filename, master))
        except (AttributeError, ValueError):
            raise PasswordError

    def get_handles(self, master):
        """Get all handles in database in tuple with popularity value.

        Arguments:
        master - the master password.
        Reurns:
        a list of tuples, one for each password
        [(popularity value, password)]"""
        data = self.load(master)
        return [(data[handle][0], handle) for handle in data.keys()] 

      
    def get_password(self, handle, master):
        """Return the password for given handle.
        Increment handle's popularity value.

        Arguments:
        handle - the handle for the password.
        Returns:
        the password.
        """
        self.mutex.acquire()
        data = self.load(master)
        data[handle] = [data[handle][0]+1, data[handle][1]]
        self.save(data, master)
        self.mutex.release()
        return data[handle][1]
    
    def add_handle(self, handle, password, master):
        """Add or replace handle in database.

        Arguments:
        handle -- the handle to add/replace.
        """
        self.mutex.acquire()
        data = self.load(master)
        if handle in data:
            data[handle] = [data[handle][0], password]
        else:
            data[handle] = [0, password]
        self.save(data, master)
        self.mutex.release()

    
    def delete_handle(self, handle, master):
        """Delete handle from database.

        Arguments:
        handle -- the handle to delete.
        """
        self.mutex.acquire()
        data = self.load(master)
        del data[handle]
        self.save(data, master)
        self.mutex.release()

    
    def change_master(self, old_master, new_master):
        """Change the master password.
        
        Arguments:
        old_master -- the old master password
        new_master -- the new master password
        """
        self.mutex.acquire()
        data = self.load(old_master)
        self.save(data, new_master)
        self.mutex.release()

class PasswordError(Exception):
    pass

