
"""
timeout.py

Re-triggerable timeout with callback for tkinter.

Tom Clayton - 2021
"""

import time

RESOLUTION = 1000 # in ms

class Timeout(object):
    """Class for re-triggerable tkinter timeout.

    Arguments:
    tkinter_root -- tkinter root object
    timeout -- (int) timeout delay in seconds
    callback -- function to be called on timeout"""
    def __init__(self, tkinter_root, timeout, callback):
        """Set tkinter root object, timeout length and callback."""
        self.tkinter_root = tkinter_root
        self.callback = callback
        self.timeout = timeout
        self.timer = 0

    def trigger(self):
        """Start/re-trigger the timeout."""
        self.timer = time.time() + self.timeout
        self.tkinter_root.after(RESOLUTION, self.check)

    def check(self):
        """Check time out and setup recurring check."""
        if self.timer:
            if time.time() > self.timer:
                self.timer = 0
                self.callback()       
            else:
                self.tkinter_root.after(RESOLUTION, self.check)

    
