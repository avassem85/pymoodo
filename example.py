from pymoodo import Controller
import asyncio
import sys
import logging

logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m %H:%M',
                    level=logging.DEBUG)

async def main(email, password):
    controller = await Controller(email, password)

    # Turn on MoodoBox
    for id in controller.boxes:
        controller.boxes[id].turn_on(100)
        # controller.boxes[id].set_fan_speed(21)

        controller.boxes[id].slots[0].set_fan_speed(100)
        controller.boxes[id].slots[1].set_fan_speed(100)
        controller.boxes[id].slots[2].set_fan_speed(100)
        controller.boxes[id].slots[3].set_fan_speed(100)

        for slot_id in controller.boxes[id].slots:
            slot = controller.boxes[id].slots[slot_id]
            slot.turn_on()
            slot.set_fan_speed(100)

        for slot_id in controller.boxes[id].slots:
            slot = controller.boxes[id].slots[slot_id]
            slot.turn_off()

        controller.boxes[id].turn_off()

        while True:
            pass

if __name__ == "__main__":
    if len(sys.argv) == 3:
        asyncio.get_event_loop().run_until_complete(main(sys.argv[1], sys.argv[2]))
    else:
        print('Run example with arguments <email> <password>')