# RPiano

## About
I made this program to learn about the WS2812 LED and Tkinter. 
This program simulates a piano keyboard from C3 to B4. 
When a piano key is clicked in the GUI, a note will be played out from the buzzer and a LED pattern will be lit according to that piano key.

## Hardware list
1. Raspberry Pi (Rpi)
2. WS2812 LED strip
3. External power supply (PSU)
4. Buzzer speaker
## Wiring 
### 1. Raspberry Pi + LED strip + External Power Supply  

![](https://i.imgur.com/DyTIWSr.png)  
* LED strip data line (blue) <-> RPi GPIO18 
* LED strip ground line (black) <-> RPi GND pin <-> PSU negative voltage pole
* LED strip positive voltage line (red) <-> PSU positive voltage pole

### 2. Raspberry Pi + Buzzer speaker

![](https://i.imgur.com/2E3f8Dt.png)  
* Buzzer speaker positive line (red) <-> RPi GPIO18 
* Buzzer speaker negative line (black) <-> RPi GND pin

### 3. Complete circuit image
![](https://i.imgur.com/Y2ECQ4u.png)

## LED strip full color pattern
The LED strip has 7 colors divided equally along its length. Each LED has this permanent color and will only light up when an applicable piano key is pressed

## Pinano GUI (made from Tkinter)
![](https://i.imgur.com/06PxkaF.png)

## Demo
![Test out each piano key](https://youtu.be/HicM2cFlmWk)  
![Happy Birthday song demo](https://youtu.be/9z8fDm4T_ZU)

## References and credits
1.	[Connect and Control WS2812 RGB LED Strips via Raspberry Pi](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/)
2.	[Hexabitz Piano Controllable from Raspberry Pi and Python GUI](https://www.hackster.io/aula-jazmati/hexabitz-piano-controllable-from-raspberry-pi-and-python-gui-c69ea6)
