
"""
timeout.py

Re-triggerable timeout with callback.

Tom Clayton - 2021
"""

import time
import threading

RESOLUTION = 1 # in s

class Timeout(object):
    def __init__(self, timeout, callback):
        self.callbacks = [callback]
        self.timeout = timeout
        self.timer = 0
        thread = threading.Thread(target=self.check, daemon=True)
        thread.start()
        

    def trigger(self):
        """Start/re-trigger the timeout."""
        self.timer = time.time() + self.timeout

    def add_callback(self, callback):
        """add a callback."""
        self.callbacks.append(callback)

    def check(self):
        """Check time out and setup recurring check."""
        while(True):
            time.sleep(RESOLUTION)
            if self.timer and time.time() > self.timer:
                self.timer = 0
                for callback in self.callbacks:
                    callback()       


    
