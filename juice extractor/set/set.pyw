import json
class key:
    def __init__(self,keys,event):
        self.keys = list(keys) 
        self.event = event 
    def press(self,down_keys):
        r=1
        for key in self.keys:
            r=r and key in down_keys
        return r