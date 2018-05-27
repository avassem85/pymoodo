from pymoodo import Controller
import asyncio

async def main():
    controller = Controller('<email>', '<password>')

    # Turn on MoodoBox
    for id in controller.boxes:
        controller.boxes[id].turn_on()
        controller.boxes[id].set_fan_speed(50)

        for slot_id in controller.boxes[id].slots:
            slot = controller.boxes[id].slots[slot_id]
            slot.turn_on()
            slot.set_fan_speed(75)
            slot.turn_off()

        controller.boxes[id].turn_off()

asyncio.get_event_loop().run_until_complete(main())