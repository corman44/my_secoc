import threading
import time

class FVM:
    def __init__(self):
        self.counter = 0
        self.last_count = 0
        self.running = True
        # create thread for 'increment'ing
        self.thread = threading.Thread(target=self._increment, daemon=True)

    def _increment(self):
        """ internal method for incrementing counter """
        while self.running:
            time.sleep(1)
            self.ffv += 1

    def sync_ffv(self, rx_tfv):
        # basic for now
        self.counter = rx_tfv + self.counter & 4278190080 # 
        pass
