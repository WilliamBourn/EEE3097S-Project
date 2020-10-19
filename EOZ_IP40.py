#Import Libraries
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error: RPi.GPIO not found")
    sys.exit(1)
from timeit import default_timer as timer
import time

#-----------------------------------------------
#Variables
#-----------------------------------------------

#Constants
#-----------------------------------------------
#TO DO: Add more default options
#TO DO: Add explanation for pins

DEFAULT_SHORT_PRESS_KEYSET = ['1','2','3','4','5','6','7','8','9','*','0','#']
DEFAULT_LONG_PRESS_KEYSET = ['A','B','C','D','E','F','G','H','I','J','K','L']
DEFAULT_COLUMN_PINSET = [11,13,15,19] #x1,x2,x3,interupt
DEFAULT_ROW_PINSET = [16,18,22,24] #y1,y2,y3,y4

DEFAULT_BOUNCETIME = 400

#Global Variables
#-----------------------------------------------
#TO DO: Implement buffer and keysets

key_buffer = []
short_press_keyset = DEFAULT_SHORT_PRESS_KEYSET
long_press_keyset = DEFAULT_LONG_PRESS_KEYSET
column_pinset = []
row_pinset = []

#Flags
#-----------------------------------------------
#TO DO: implement these properly
long_press_en = False
key_buffer_en = False

#-----------------------------------------------
#Functions
#-----------------------------------------------

#Setup Functions
#-----------------------------------------------
#TO DO: Add options for initialization, such as setting bouncetime, allowing inverting of pins (outputs default low, inputs pulled up)
#TO DO: Figure out how to work with multiple function definitions (not sure if this works in Python)
#TO DO: Add methods for initializing keysets and other things


#Initialize all the GPIO pins that the keypad uses and assign callbacks
#def initialize_gpio():
#    #Call function of same name with default arguments 
#    initialize_keypad(DEFAULT_COLUMN_PINSET,DEFAULT_ROW_PINSET)

#Initialize all the GPIO pins that the keypad uses and assign callbacks, takes custom pinsets
def initialize_gpio(new_column_pinset,new_row_pinset):
    global column_pinset, row_pinset
    
    column_pinset = new_column_pinset
    row_pinset = new_row_pinset
    
    print(column_pinset)
    print(row_pinset)
    
    #Set GPIO mode to board
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    
    #Initialize column pins as input pins that are pulled down
    GPIO.setup(column_pinset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    #Initialize row pins as output pins with a default high logic value
    GPIO.setup(row_pinset, GPIO.OUT)
    GPIO.output(row_pinset, GPIO.HIGH)
    
    #Add interupt callback to column pins
    GPIO.add_event_detect(column_pinset[3], GPIO.RISING, bouncetime=DEFAULT_BOUNCETIME)
    GPIO.add_event_callback(column_pinset[3], press_event)


#Initialize all the GPIO pins that the keypad uses and assign callbacks, independant pins
#def initialize_gpio(column1=DEFAULT_COLUMN_PINSET[0],column2=DEFAULT_COLUMN_PINSET[1],column3=DEFAULT_COLUMN_PINSET[2],row1=DEFAULT_ROW_PINSET[0],row2=DEFAULT_ROW_PINSET[1],row3=DEFAULT_ROW_PINSET[2],row4=DEFAULT_ROW_PINSET[3]):
#    column_pinset = [column1,column2,column3]
#    row_pinset = [row1,row2,row3,row4]

    
#Callback Functions
#-----------------------------------------------
#TO DO: Figure out how to reduce the number of bad inputs. Maybe adjust sleep time? Maybe add an interupt for the columns?
#TO DO: Implement long press functionality
    
#Interupt function that triggers when a button is pressed
def press_event(channel):
    column_pin = None
    row_pin = None
    press_start = None
    press_stop = None
    
    
    #Throw an exception if you cannot determine the input        
    try:        
        #Skip if long presses are disabled
        if long_press_en:
            press_start = timer()
    
        #Identify the colum pin that triggered the event
        for pin in column_pinset:
            if (pin != channel) & (GPIO.input(pin) == GPIO.HIGH):
                column_pin = pin
                break
        
        #Identify the row pin that triggered the event
        for pin in row_pinset:
            GPIO.output(pin, GPIO.LOW)
            if GPIO.input(column_pin) == GPIO.LOW:
                row_pin = pin
                GPIO.output(pin, GPIO.HIGH)
                break                
    
        #Skip if long presses are disabled
        if long_press_en:
            GPIO.wait_for_edge(column_pin, GPIO.FALLING)
            press_end = timer()
            if (press_end - press_start) > long_press_delay:
                pass        #Implement long presses here

        #Reset the GPIO pins
        GPIO.output(row_pinset,GPIO.HIGH)
        
        
        
        #Get a pair of values that, when added together map to the correct key
        column = None
        row = None
        if column_pin == column_pinset[0]:
            column = 0
        elif column_pin == column_pinset[1]:
            column = 1
        elif column_pin == column_pinset[2]:
            column = 2
        else:
            raise Exception("Invalid pin")

        if row_pin == row_pinset[0]:
            row = 0
        elif row_pin == row_pinset[1]:
            row = 3
        elif row_pin == row_pinset[2]:
            row = 6
        elif row_pin == row_pinset[3]:
            row = 9
        else:
            raise Exception("Invalid pin")

        add_to_buffer(short_press_keyset[row+column])

        #Sleep to prevent overlapping inputs
        time.sleep(0.2)
                
        

    except Exception as e:
        print("Bad input")
        GPIO.output(row_pinset, GPIO.HIGH)
    
         
    
#Key buffer functions
#-----------------------------------------------
#TO DO: Implement the key buffer proper

#Enable the key buffer to hold more than one key
def enable_key_buffer(bool):
    key_buffer_en = bool

#Push a new key into the buffer
def add_to_buffer(char):
    if key_buffer_en:
        key_buffer.append(char)
    key_buffer = [char]
    print(char)

#Fetch the next key from the buffer, if there is not key in the buffer, then return a tab
def fetch_next():
    #Check if there is a key in the buffer
    if len(key_buffer) > 0:
        return key_buffer.pop(0)
    else:
        return '\t'



#Enable a different keyset to be used when a button is held for longer
def enable_long_press_event(bool):
    pass


#Main function
#-----------------------------------------------
#Dispose of this when done. Shouldn't be part of library, is only for testing

if __name__ == "__main__":
    try:
        initialize_gpio(DEFAULT_COLUMN_PINSET,DEFAULT_ROW_PINSET)
        print(short_press_keyset)
        while True:
            pass
    
    except Exception as e:
        print(e) 
#adding a testing comment at the end so i can push the code -Declan

