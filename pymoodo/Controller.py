from .Connection import Connection
from .Models import MoodoBox

class Controller:
    def __init__(self, email=None, password=None):
        self.__connection = Connection(email, password)
        self.boxes = {}
        if self.__connection.authenticated:
            self.update_boxes()
        else:
            print("Could not connect to Moody API")
    
    @property
    def authenticated(self):
        """Return the display name of this light."""
        return self.__connection.authenticated

    def update_boxes(self):
        boxes = self.get_boxes()
        for box in boxes['boxes']:
             self.boxes[box['id']] = MoodoBox(box, self)
        return self.boxes
        
    def get_boxes(self):
        return self.__connection.get('/boxes')

    def get_box(self, device_key):
        return self.__connection.get('/boxes/%s' % (device_key))

    def post_box(self, device_key, box):
        data = {
            'device_key': box['device_key'],
            'fan_volume': box['fan_volume'],
            'box_status': box['box_status'],
            'settings_slot0': {
                'fan_speed': box['settings'][0]['fan_speed'],
                'fan_active': box['settings'][0]['fan_active']
            },
            'settings_slot1': {
                'fan_speed': box['settings'][1]['fan_speed'],
                'fan_active': box['settings'][1]['fan_active']
            },
            'settings_slot2': {
                'fan_speed': box['settings'][2]['fan_speed'],
                'fan_active': box['settings'][2]['fan_active']
            },
            'settings_slot3': {
                'fan_speed': box['settings'][3]['fan_speed'],
                'fan_active': box['settings'][3]['fan_active']
            }
        }

        return self.__connection.post('/boxes', data)

    def post_shuffle(self, device_key):
        return self.__connection.post('/shuffle/%s' % (device_key))

    def delete_shuffle(self, device_key):
        return self.__connection.delete('/shuffle/%s' % (device_key))


