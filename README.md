# EEE3097S-Project

Quick Setup instructions:

Viewing the keypad from the back, pins are 0-6 from left to right.

Keypad pins 0,1,2 connect to RPi pins 15,13,11 respectfully. The anode of a diode is connected to each of these pins, the cathode connects to pin 19.
Keypad pins 3,4,5,6 connect to RPi pins 24,22,18,16.

If it is all set up correctly, then when you run EOZ_IP40.py, it will display the pins you should be using, then the set of chars attached to each button. By pressing buttons
on the keypad, the command line should print the assigned character. Press ctrl+C to exit this test function.