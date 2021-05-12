import socketio
import logging
from asyncinit import asyncinit

_LOGGER = logging.getLogger(__name__)

@asyncinit
class WebsocketConnection(object):
    sio = socketio.AsyncClient()

    async def __init__(self, controller, token, boxes):
        self.call_backs()
        self.controller = controller
        self.__token = token
        self.__boxes = boxes
        self.__ws_url = 'https://ws.moodo.co:9090'
        await self.sio.connect(self.__ws_url)

    async def process_ws_events(self): 
        await self.sio.wait()

    def call_backs(self):

        @self.sio.event
        async def connect():
            _LOGGER.info(f'Connection established with {self.__ws_url}')
            await self.sio.emit('authenticate', (self.__token, 'false'))
            
        @self.sio.event
        async def log(data):
            if "Authenticated account:" in data:
                _LOGGER.info('Successfully authenticated with account %s', data[23:])
                for box in self.__boxes:
                    await self.sio.emit('subscribe', (box, 'false'))
            elif "Subscribed to events of box with device key:" in data:
                _LOGGER.info('Successfully subscribed to events of box with device key: %s', data[45:])
            else:
                _LOGGER.warning('Can\'t process log event with data: %s', data)
            

        @self.sio.event
        async def ws_event(data):
            if data['type'] == 'box_config':
                self.controller.update_box(data['data'])
            else:
                _LOGGER.warning('Can\'t process ws_event with data: %s', data)

        @self.sio.event
        async def disconnect():
            _LOGGER.info('Disconnected from server')