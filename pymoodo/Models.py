import logging

_LOGGER = logging.getLogger(__name__)

class MoodoBox:
    """Represents a MoodoBox."""

    def __init__(self, box, controller):
        self.id = box['id']
        self.__controller = controller
        self.__box = box
        self.slots = {}
        self.__processslots()

    def update(self, box):
        self.__box = box
        _LOGGER.info('Box with key %s updated by ws_event', self.device_key)
        self.log()

    def __processslots(self):
        for slot in self.__box['settings']:
            self.slots[slot['slot_id']] = MoodoBoxSlot(slot, self.__box, self.__controller, self)

    def log(self):
        _LOGGER.debug('# MoodoBox: %s (id: %s, key: %s) - Active: %s - Speed: %s' % (self.name, self.id, self.device_key, self.status, self.fan_speed))
        self.slots[0].log()
        self.slots[1].log()
        self.slots[2].log()
        self.slots[3].log()
    
    @property
    def device_key(self):
        return self.__box['device_key']

    @property
    def name(self):
        return self.__box['name']
    
    @property
    def fan_speed(self):
        return self.__box['fan_volume']

    @property
    def status(self):
        return self.__box['box_status']

    @property
    def is_online(self):
        return self.__box['is_online']

    @property
    def is_adapter_on(self):
        return self.__box['is_adapter_on']

    @property
    def is_battery_charging(self):
        return self.__box['is_battery_charging']

    @property
    def shuffle(self):
        return self.__box['shuffle']

    @property
    def interval(self):
        return self.__box['interval']

    @property
    def interval_type(self):
        return self.__box['interval_type']

    def turn_on(self, speed=None):
        box = self.__box
        if box['is_online']:
            box['box_status'] = 1
            if speed is not None:
                box['fan_volume'] = speed
            self.__controller.post_box(self.device_key, box)
        else:
            _LOGGER.error('Moodobox is not online')

    def turn_off(self):
        box = self.__box 
        if box['is_online']:     
            box['box_status'] = 0
            self.__controller.delete_box(self.device_key)
        else:
            _LOGGER.error('Moodobox is not online')

    def enable_shuffle(self):
        box = self.__box 
        if box['is_online']: 
            self.__controller.post_shuffle(self.device_key)
        else:
            _LOGGER.error('Moodobox is not online')

    def disable_shuffle(self):
        box = self.__box 
        if box['is_online']: 
            self.__controller.delete_shuffle(self.device_key)
        else:
            _LOGGER.error('Moodobox is not online')

    def set_fan_speed(self, speed):
        box = self.__box
        if box['is_online']:
            box['fan_volume'] = speed
            box = self.__controller.post_intensity(self.device_key, box)
        else:
            _LOGGER.error('Moodobox is not online')

class MoodoBoxSlot:
    """Represents a Capsule in the MoodoBox."""

    def __init__(self, slot, box, controller, moodobox):
        self.id = slot['slot_id']
        self.__slot = slot
        self.__box = box
        self.__controller = controller
        self.__moodobox = moodobox

    def log(self):
        _LOGGER.debug('= Capsule: %s(#%s) - Active: %s - Speed: %s' % (self.scent, self.code, self.fan_active, self.fan_speed))

    @property
    def code(self):
        return self.__slot['capsule_type_code']

    @property
    def color(self):
        return self.__slot['capsule_info']['color']

    @property
    def scent(self):
        return self.__slot['capsule_info']['title']

    @property
    def fan_speed(self):
        return self.__slot['fan_speed']

    @property
    def fan_active(self):
        return self.__slot['fan_active']

    @property
    def fan_working_hours(self):
        return self.__slot['fan_working_hours']

    @property
    def fan_speed_absolute(self):
        return self.__slot['fan_speed_absolute']

    @property
    def fan_speed_relative(self):
        return self.__slot['fan_speed_relative']

    def turn_on(self):
        box = self.__box 
        if box['is_online']: 
            box['settings'][self.id]['fan_active'] = True   
            self.__controller.post_boxes(self.id, box)
        else:
            _LOGGER.error('Moodobox is not online')

    def turn_off(self):
        box = self.__box 
        if box['is_online']:
            box['settings'][self.id]['fan_active'] = False
            self.__controller.post_boxes(self.id, box)
        else:
            _LOGGER.error('Moodobox is not online')

    def set_fan_speed(self, speed):
        box = self.__box 
        if box['is_online']: 
            box['settings'][self.id]['fan_active'] = True
            box['settings'][self.id]['fan_speed'] = speed        
            self.__controller.post_boxes(self.id, box)
        else:
            _LOGGER.error('Moodobox is not online')