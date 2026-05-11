import threading
import time

class FVM:
    def __init__(self):
        self.running = True
        self.counters = {} # dict of all messages and corresponding FV {msg_id: full_fv}
        self.last_count = {} # dict of all previous full_fvs based on msg_id
        # create thread for 'increment'ing
        self.thread = threading.Thread(target=self._increment, daemon=True)

    def _increment(self):
        # internal method for incrementing counters
        while self.running:
            time.sleep(1)
            for msg_id, ffv in self.counters.items():
                self.last_count[msg_id] = self.counters[msg_id]
                self.counters[msg_id] += 1

    def sync_counter(self, rx_msg_id, rx_tfv):
        # set last count value
        self.last_count[rx_msg_id] = self.counters[rx_msg_id]
        
        # update counter
        self.counters[rx_msg_id] = rx_tfv + (self.counter[rx_msg_id] & 4278190080) # 
        pass
