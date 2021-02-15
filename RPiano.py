from tkinter import *
import tkinter.font
import RPi.GPIO
from functools import partial
from rpi_ws281x import *
import time

RPi.GPIO.setmode(RPi.GPIO.BCM) #Use the Broadcom method for naming the GPIO pins
buzzer_pin = 22                   #set the buzzer pin variable to number 22
RPi.GPIO.setup(buzzer_pin, RPi.GPIO.OUT)  #Set pin 22 as an output pin

notes = {
    'C3' : 131, 'CS3' : 139,
    'D3' : 147, 'DS3' : 156,
    'EB3' : 156,
    'E3' : 165,
    'F3' : 175, 'FS3' : 185,
    'G3' : 196, 'GS3' : 208,
    'A3' : 220, 'AS3' : 233,
    'BB3' : 233,
    'B3' : 247,
    'C4' : 262, 'CS4' : 277,
    'D4' : 294, 'DS4' : 311,
    'EB4' : 311,
    'E4' : 330,
    'F4' : 349, 'FS4' : 370,
    'G4' : 392, 'GS4' : 415,
    'A4' : 440, 'AS4' : 466,
    'BB4' : 466,
    'B4' : 494,
    }

### LED strip configuration: ###
LED_COUNT      = 296      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#### Functions ####
duration = 0.1
def buzz(pitch):   #create the function "buzz" and feed it the pitch and duration)
 period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
 delay = period / 2     #calcuate the time for half of the wave
 cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency
 for i in range(cycles):    #start a loop from 0 to the variable "cycles" calculated above
   RPi.GPIO.output(buzzer_pin, True)   #set pin 22 to high
   time.sleep(delay)    #wait with pin 22 high
   RPi.GPIO.output(buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 22 low


steps=25
interval=0.001
def fade_in(start_pixel,end_pixel, note, event):
    lastUpdate = time.time() - interval
    for i in range(1, steps + 1):
        for j in range(strip.numPixels()):
            if start_pixel <= j <= end_pixel:
                r = color_dict[j]["r"] * i // steps
                g = color_dict[j]["g"] * i // steps
                b = color_dict[j]["b"] * i // steps
            else:
                r = 0
                g = 0
                b = 0
            while ((time.time() - lastUpdate) < interval):
                pass
            color = Color(r, g, b)
            strip.setPixelColor(j, color)
        strip.show()
        lastUpdate = time.time()
    buzz(note)
def fade_out(start_pixel,end_pixel, event):
    lastUpdate = time.time() - interval
    for i in range(1, steps + 1):
        for j in range(strip.numPixels()):
            if start_pixel <= j <= end_pixel:
                r = color_dict[j]["r"] * (steps - i) // steps
                g = color_dict[j]["g"] * (steps - i) // steps
                b = color_dict[j]["b"] * (steps - i) // steps
            else:
                r = 0
                g = 0
                b = 0
            while ((time.time() - lastUpdate) < interval):
                pass
            color = Color(r, g, b)
            strip.setPixelColor(j, color)
        strip.show()
        lastUpdate = time.time()

def close():
    RPi.GPIO.cleanup()
    win.destroy()


### set rainbow color functions ###

def color_dict(strip):
    color_dict = {}
    for pos in range(strip.numPixels()):        
        if pos < 37:
            color_dict[pos] = {"r":255, "g":0, "b": 0} #red 
        elif pos < 37*2:
            color_dict[pos] = {"r":255, "g":127, "b": 0} #orange
        elif pos < 37*3:
            color_dict[pos] = {"r":255, "g":255, "b": 0} #yellow
        elif pos < 37*4:
            color_dict[pos] = {"r":0, "g":255, "b": 0} #green   
        elif pos < 37*5:
            color_dict[pos] = {"r":0, "g":255, "b": 255} #cyan     
        elif pos < 37*6:
            color_dict[pos] = {"r":0, "g":0, "b": 255} #blue
        else:
            color_dict[pos] = {"r":127, "g":0, "b": 255} #purple          
    return color_dict

def rainbow(strip):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(color_dict[i]["r"],color_dict[i]["g"],color_dict[i]["b"]))
    strip.show()

### Main Program ###
    
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()    
# Map rainbow color code to each led
color_dict = color_dict(strip)

### GUI DEFINITIONS ###
win = Tk()
win.title("Piano")
myFont = tkinter.font.Font(family = 'Helvetica', size = 1)

scales = 2
win.geometry('{}x200'.format(300 * scales))

key_C3 = Button(win, bg='white', activebackground='gray87', text='C3', width=1, anchor="s")
key_C3.grid(row=0, column=0, rowspan=4, columnspan=3, sticky='nsew')
key_C3.bind('<ButtonPress>',   partial(fade_in,0,21, notes["C3"]))
key_C3.bind('<ButtonRelease>', partial(fade_out,0,21))

key_D3 = Button(win, bg='white', activebackground='gray87', text='D3', width=1, anchor="s")
key_D3.grid(row=0, column=3, rowspan=2, columnspan=3, sticky='nsew')
key_D3.bind('<ButtonPress>',   partial(fade_in,22,42, notes["D3"])) 
key_D3.bind('<ButtonRelease>', partial(fade_out,22,42))

key_E3 = Button(win, bg='white', activebackground='gray87', text='E3', width=1, anchor="s")
key_E3.grid(row=0, column=6, rowspan=2, columnspan=3, sticky='nsew')
key_E3.bind('<ButtonPress>',   partial(fade_in,43,63, notes["E3"])) 
key_E3.bind('<ButtonRelease>', partial(fade_out,43,63))

key_F3 = Button(win, bg='white', activebackground='gray87', text='F3', width=1, anchor="s")
key_F3.grid(row=0, column=9, rowspan=2, columnspan=3, sticky='nsew')
key_F3.bind('<ButtonPress>',   partial(fade_in,64,84, notes["F3"])) 
key_F3.bind('<ButtonRelease>', partial(fade_out,64,84))

key_G3 = Button(win, bg='white', activebackground='gray87', text='G3', width=1, anchor="s")
key_G3.grid(row=0, column=12, rowspan=2, columnspan=3, sticky='nsew')
key_G3.bind('<ButtonPress>',   partial(fade_in,85,105, notes["G3"])) 
key_G3.bind('<ButtonRelease>', partial(fade_out,85,105))

key_A3 = Button(win, bg='white', activebackground='gray87', text='A3', width=1, anchor="s")
key_A3.grid(row=0, column=15, rowspan=2, columnspan=3, sticky='nsew')
key_A3.bind('<ButtonPress>',   partial(fade_in,106,126, notes["A3"])) 
key_A3.bind('<ButtonRelease>', partial(fade_out,106,126))

key_B3 = Button(win, bg='white', activebackground='gray87', text='B3', width=1, anchor="s")
key_B3.grid(row=0, column=18, rowspan=2, columnspan=3, sticky='nsew')
key_B3.bind('<ButtonPress>',   partial(fade_in,127,147, notes["B3"])) 
key_B3.bind('<ButtonRelease>', partial(fade_out,127,147))

key_C4 = Button(win, bg='white', activebackground='gray87', text='C4', width=1, anchor="s")
key_C4.grid(row=0, column=21, rowspan=2, columnspan=3, sticky='nsew')
key_C4.bind('<ButtonPress>',   partial(fade_in,148,168, notes["C4"])) 
key_C4.bind('<ButtonRelease>', partial(fade_out,148,168))

key_D4 = Button(win, bg='white', activebackground='gray87', text='D4', width=1, anchor="s")
key_D4.grid(row=0, column=24, rowspan=2, columnspan=3, sticky='nsew')
key_D4.bind('<ButtonPress>',   partial(fade_in,169,189, notes["D4"])) 
key_D4.bind('<ButtonRelease>', partial(fade_out,169,189))

key_E4 = Button(win, bg='white', activebackground='gray87', text='E4', width=1, anchor="s")
key_E4.grid(row=0, column=27, rowspan=2, columnspan=3, sticky='nsew')
key_E4.bind('<ButtonPress>',   partial(fade_in,190,210, notes["E4"])) 
key_E4.bind('<ButtonRelease>', partial(fade_out,190,210))

key_F4 = Button(win, bg='white', activebackground='gray87', text='F4', width=1, anchor="s")
key_F4.grid(row=0, column=30, rowspan=2, columnspan=3, sticky='nsew')
key_F4.bind('<ButtonPress>',   partial(fade_in,211,231, notes["F4"])) 
key_F4.bind('<ButtonRelease>', partial(fade_out,211,231))

key_G4 = Button(win, bg='white', activebackground='gray87', text='G4', width=1, anchor="s")
key_G4.grid(row=0, column=33, rowspan=2, columnspan=3, sticky='nsew')
key_G4.bind('<ButtonPress>',   partial(fade_in,232,252, notes["G4"])) 
key_G4.bind('<ButtonRelease>', partial(fade_out,232,252))

key_A4 = Button(win, bg='white', activebackground='gray87', text='A4', width=1, anchor="s")
key_A4.grid(row=0, column=36, rowspan=2, columnspan=3, sticky='nsew')
key_A4.bind('<ButtonPress>',   partial(fade_in,253,273, notes["A4"])) 
key_A4.bind('<ButtonRelease>', partial(fade_out,253,273))

key_B4 = Button(win, bg='white', activebackground='gray87', text='B4', width=1, anchor="s")
key_B4.grid(row=0, column=39, rowspan=2, columnspan=3, sticky='nsew')
key_B4.bind('<ButtonPress>',   partial(fade_in,274,295, notes["B4"])) 
key_B4.bind('<ButtonRelease>', partial(fade_out,274,295))

key_C3S = Button(win, bg='black', activebackground='gray12')
key_C3S.grid(row=0, column=(0*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_C3S.bind('<ButtonPress>',   partial(fade_in,10,31, notes["CS3"])) 
key_C3S.bind('<ButtonRelease>', partial(fade_out,10,31))

key_D3S = Button(win, bg='black', activebackground='gray12')
key_D3S.grid(row=0, column=(1*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_D3S.bind('<ButtonPress>',   partial(fade_in,32,52, notes["DS3"])) 
key_D3S.bind('<ButtonRelease>', partial(fade_out,32,52))

key_F3S = Button(win, bg='black', activebackground='gray12')
key_F3S.grid(row=0, column=(3*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_F3S.bind('<ButtonPress>',   partial(fade_in,74,94, notes["FS3"])) 
key_F3S.bind('<ButtonRelease>', partial(fade_out,74,94))

key_G3S = Button(win, bg='black', activebackground='gray12')
key_G3S.grid(row=0, column=(4*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_G3S.bind('<ButtonPress>',   partial(fade_in,95,115, notes["GS3"])) 
key_G3S.bind('<ButtonRelease>', partial(fade_out,95,115))

key_A3S = Button(win, bg='black', activebackground='gray12')
key_A3S.grid(row=0, column=(5*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_A3S.bind('<ButtonPress>',   partial(fade_in,116,136, notes["AS3"])) 
key_A3S.bind('<ButtonRelease>', partial(fade_out,116,136))

key_C4S = Button(win, bg='black', activebackground='gray12')
key_C4S.grid(row=0, column=(7*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_C4S.bind('<ButtonPress>',   partial(fade_in,158,178, notes["CS4"])) 
key_C4S.bind('<ButtonRelease>', partial(fade_out,158,178))

key_D4S = Button(win, bg='black', activebackground='gray12')
key_D4S.grid(row=0, column=(8*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_D4S.bind('<ButtonPress>',   partial(fade_in,179,199, notes["DS4"])) 
key_D4S.bind('<ButtonRelease>', partial(fade_out,179,199))

key_F4S = Button(win, bg='black', activebackground='gray12')
key_F4S.grid(row=0, column=(10*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_F4S.bind('<ButtonPress>',   partial(fade_in,221,241, notes["FS4"])) 
key_F4S.bind('<ButtonRelease>', partial(fade_out,221,241))

key_G4S = Button(win, bg='black', activebackground='gray12')
key_G4S.grid(row=0, column=(11*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_G4S.bind('<ButtonPress>',   partial(fade_in,242,262, notes["GS4"])) 
key_G4S.bind('<ButtonRelease>', partial(fade_out,242,262))

key_A4S = Button(win, bg='black', activebackground='gray12')
key_A4S.grid(row=0, column=(12*3)+2, rowspan=1, columnspan=2, sticky='nsew')
key_A4S.bind('<ButtonPress>',   partial(fade_in,263,283, notes["AS4"])) 
key_A4S.bind('<ButtonRelease>', partial(fade_out,263,283))


for i in range(7* scales * 3):
    win.columnconfigure(i, weight=1)

for i in range(2):
    win.rowconfigure(i, weight=1)

win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO when user closes window
win.mainloop()

