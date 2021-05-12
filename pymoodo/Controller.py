import asyncio
import threading
import logging
from asyncinit import asyncinit
from .HTTPConnection import HTTPConnection
from .WebsocketConnection import WebsocketConnection
from .Models import MoodoBox

_LOGGER = logging.getLogger(__name__)

@asyncinit
class Controller:
    async def __init__(self, email=None, password=None):
        # self.thread = threading.Thread(target=self.process_ws_events)
        self.__httpconnection = HTTPConnection(email, password)
        self.boxes = {}
        if self.__httpconnection.authenticated:
            boxes = self.get_boxes()
            for box in boxes['boxes']:
                self.boxes[box['id']] = MoodoBox(box, self)
                self.thread = threading.Thread(target=asyncio.run, args=(self.process_ws_events(self.boxes),))
                self.thread.setDaemon(True)
                self.thread.start()
        else:
            _LOGGER.error("Could not connect to Moody API")

    async def process_ws_events(self, box):
        self.__wsconnection = await WebsocketConnection(self, self.__httpconnection.token, box)
        await self.__wsconnection.process_ws_events()
    
    @property
    def authenticated(self):
        """Return the display name of this light."""
        return self.__httpconnection.authenticated

    def update_box(self, data):
        self.boxes[data['id']].update(data)
        
    def get_boxes(self):
        return self.__httpconnection.get('/boxes')

    def get_box(self, device_key):
        return self.__httpconnection.get('/boxes/%s' % (device_key))

    def post_box(self, device_key, box):
        data = {
            'fan_volume': box['fan_volume']
        }

        return self.__httpconnection.post('/boxes/%s' % (device_key), data)
    
    def post_intensity(self, device_key, box):
        data = {
            'fan_volume': box['fan_volume'],
            'restful_request_id': 'string'
        }

        return self.__httpconnection.post('/intensity/%s' % (device_key), data)

    def delete_box(self, device_key):
        return self.__httpconnection.delete('/boxes/%s' % (device_key))

    def post_boxes(self, device_key, box):
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

        return self.__httpconnection.post('/boxes', data)

    def put_boxes(self, device_key, box, duration=None):
        data = {
            'device_key': box['device_key'],
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
            },
            "restful_request_id": "string"
        }
        if duration is not None:
            data['duration_seconds'] = duration

        return self.__httpconnection.put('/boxes', data)

    def post_shuffle(self, device_key):
        return self.__httpconnection.post('/shuffle/%s' % (device_key))

    def delete_shuffle(self, device_key):
        return self.__httpconnection.delete('/shuffle/%s' % (device_key))


