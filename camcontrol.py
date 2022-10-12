# MIDI to AW-HE50S PT camera controller
# Made by Max Hunter for Francis Clegg / Snarky Puppy, 2022

import pygame.midi
import requests

# CHANGE THIS LINE TO THE CORRECT MIDI INPUT
midi_input_id = 4

cam_ip_base = "192.168.0."
cam_0_ip = 10

pygame.midi.init()

def move2preset(cam_id, preset):
	cam_ip = cam_0_ip + cam_id

	requeststr = f"http://{cam_ip_base}{cam_ip}/cgi-bin/aw_ptz?cmd=#R{preset:02}&res=1"
	print(requeststr)
	requests.get(requeststr)

print("Found {} midi devices".format(pygame.midi.get_count()))

for i in range(pygame.midi.get_count()):
    print("#{}: {}".format(i, pygame.midi.get_device_info(i)))

midi_input = pygame.midi.Input(midi_input_id)

print("Using input #{}".format(midi_input_id))

while True:
    if not midi_input.poll():
        continue
    ev = midi_input.read(midi_input_id)
    if (ev[0][0][0] != 248): #ignore clock messages
    	note_id = ev[0][0][1]
    	note_velocity = ev[0][0][2]

    	if (note_velocity != 0):
    		print(f"Note {note_id} on, velocity {note_velocity}")

    		cam_id = note_id // 10
    		preset = note_id % 10

    		print(f"Moving camera {cam_id} to preset {preset}")
    		move2preset(cam_id, preset)

    	else:
    		print(f"Note {note_id} off")


