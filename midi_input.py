from pygame import midi

print(midi.init())
id = midi.get_default_input_id()
print(midi.get_device_info(id))

mkeys = midi.Input(id)
print(mkeys)
while True:
    if mkeys.poll():
        print(mkeys.read(20))

