class MoodoBox:
    """Represents a MoodoBox."""

    def __init__(self, box, controller):
        self.id = box['id']
        self.__controller = controller
        self.__box = box
        self.slots = {}
        self.__processslots()

    def __processslots(self):
        for slot in self.__box['settings']:
            self.slots[slot['slot_id']] = MoodoBoxSlot(slot, self.__box, self.__controller, self)

    def print(self):
        print('# MoodoBox: %s (id: %s, key: %s) - Active: %s - Speed: %s' % (self.name, self.id, self.device_key, self.status, self.fan_speed))
        self.slots[0].print()
        self.slots[1].print()
        self.slots[2].print()
        self.slots[3].print()
        print('-')
    
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
        return self.__box['box_status'] == 1

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

    def turn_on(self):
        box = self.__box    
        box['box_status'] = 1
        self.__controller.post_box(self.device_key, box)
        self.update()

    def turn_off(self):
        box = self.__box      
        box['box_status'] = 0
        self.__controller.post_box(self.device_key, box)
        self.update()

    def enable_shuffle(self):
        self.__controller.post_shuffle(self.device_key)
        self.update()

    def disable_shuffle(self):
        self.__controller.delete_shuffle(self.device_key)
        self.update()

    def set_fan_speed(self, speed):
        box = self.__box     
        box['box_status'] = 1
        box['fan_volume'] = speed
        box = self.__controller.post_box(self.device_key, box)
        self.update()

    def update(self):
        box = self.__controller.get_box(self.device_key)
        self.__box = box['box']
        self.__processslots()
        self.print()

class MoodoBoxSlot:
    """Represents a MoodoBox."""

    def __init__(self, slot, box, controller, moodobox):
        self.id = slot['slot_id']
        self.__slot = slot
        self.__box = box
        self.__controller = controller
        self.__moodobox = moodobox

    def print(self):
        print('= Capsule: %s(#%s) - Active: %s - Speed: %s' % (self.scent, self.code, self.fan_active, self.fan_speed))

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
        box['settings'][self.id]['fan_active'] = True    
        self.__controller.post_box(self.id, box)

    def turn_off(self):
        box = self.__box
        box['settings'][self.id]['fan_active'] = False   
        self.__controller.post_box(self.id, box)

    def set_fan_speed(self, speed):
        box = self.__box
        box['settings'][self.id]['fan_active'] = True
        box['settings'][self.id]['fan_speed'] = speed        
        self.__controller.post_box(self.id, box)
        self.__moodobox.update()