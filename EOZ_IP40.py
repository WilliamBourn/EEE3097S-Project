#-----------------------------------------------
#Libraries
#-----------------------------------------------

#Libraries used:
#RPi.GPIO - Standard Raspberry Pi GPIO library
#timit - Timer library for implementation of long press features

#Try to import the libraries and exit the program if some are missing
try:
    import RPi.GPIO as GPIO
    from timeit import default_timer as timer
except RuntimeError as e:
    print(e)
    sys.exit(1)

#-----------------------------------------------
#Variables
#-----------------------------------------------

#Constants
#-----------------------------------------------
#TO DO: Add more default options
#TO DO: Add explanation for pins

#Default Keysets
DEFAULT_SHORT_PRESS_KEYSET = ['1','2','3','4','5','6','7','8','9','*','0','#']
DEFAULT_LONG_PRESS_KEYSET = ['A','B','C','D','E','F','G','H','I','J','K','L']

#Default Pinsets
DEFAULT_COLUMN_PINSET = [11,13,15,19] #x1,x2,x3,interupt
DEFAULT_ROW_PINSET = [16,18,22,24] #y1,y2,y3,y4

#Default Timing Setups
DEFAULT_BOUNCETIME = 300
DEFAULT_LONG_PRESS_DELAY = 500

#Global Variables
#-----------------------------------------------
_key_buffer = []
_short_press_keyset = []
_long_press_keyset = []
_long_press_delay = []
_column_pinset = []
_row_pinset = []

#Flags
#-----------------------------------------------
_long_press_en = None
_key_buffer_en = None

#-----------------------------------------------
#Functions
#-----------------------------------------------

#Setup Functions
#-----------------------------------------------
#TO DO: Add options for initialization, such as setting bouncetime, allowing inverting of pins (outputs default low, inputs pulled up)


#Initialize all the GPIO pins that the keypad uses and assign callbacks
def initialize_gpio(column_pinset=DEFAULT_COLUMN_PINSET, row_pinset=DEFAULT_ROW_PINSET, short_press_keyset=DEFAULT_SHORT_PRESS_KEYSET, long_press_keyset=DEFAULT_LONG_PRESS_KEYSET,long_press_delay=DEFAULT_LONG_PRESS_DELAY, long_press_en=False,key_buffer_en=False):
    global _column_pinset, _row_pinset, _short_press_keyset, _long_press_keyset, _long_press_delay, _long_press_en, _key_buffer_en
    
    #Set all the global variables
    _column_pinset = column_pinset
    _row_pinset = row_pinset
    _short_press_keyset = short_press_keyset
    _long_press_keyset = long_press_keyset
    _long_press_delay = long_press_delay
    _long_press_en = long_press_en
    _key_buffer_en = key_buffer_en
        
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



    
#Callback Functions
#-----------------------------------------------
    
#Interupt function that triggers when a button is pressed
def press_event(channel):
    column_pin = None
    row_pin = None
    press_start = None
    press_stop = None
    long_press = None
    
    #Drop input if the interupt pin is no longer triggered
    if GPIO.input(channel) != GPIO.HIGH:
        return
    
    #Throw an exception if you cannot determine the input        
    try:        
        #Skip if long presses are disabled
        if _long_press_en:
            press_start = timer()
    
        #Identify the colum pin that triggered the event
        for pin in _column_pinset:
            if (pin != channel) & (GPIO.input(pin) == GPIO.HIGH):
                column_pin = pin
                break
        
        #Identify the row pin that triggered the event
        for pin in _row_pinset:
            GPIO.output(pin, GPIO.LOW)
            if GPIO.input(column_pin) == GPIO.LOW:
                row_pin = pin
                GPIO.output(pin, GPIO.HIGH)
                break                
    
        #Skip if long presses are disabled
        if _long_press_en:
            GPIO.wait_for_edge(column_pin, GPIO.FALLING)
            press_end = timer()
            if (press_end - press_start)*1000 > _long_press_delay:
                long_press = True

        #Reset the GPIO pins
        GPIO.output(_row_pinset,GPIO.HIGH)
        
        #Get a pair of values that, when added together, map to the correct key
        column_value = None
        row_value = None
        if column_pin == _column_pinset[0]:
            column_value = 0
        elif column_pin == _column_pinset[1]:
            column_value = 1
        elif column_pin == _column_pinset[2]:
            column_value = 2
        else:
            raise Exception("Invalid pin")

        if row_pin == _row_pinset[0]:
            row_value = 0
        elif row_pin == _row_pinset[1]:
            row_value = 3
        elif row_pin == _row_pinset[2]:
            row_value = 6
        elif row_pin == _row_pinset[3]:
            row_value = 9
        else:
            raise Exception("Invalid pin")

        #Choose the correct key buffer
        if long_press == True:
            add_to_buffer(_long_press_keyset[row_value+column_value])
        else:
            add_to_buffer(_short_press_keyset[row_value+column_value])     

    except Exception as e:
        print(e)
        GPIO.output(_row_pinset, GPIO.HIGH)
         
    
#Key buffer functions
#-----------------------------------------------

#Enable the key buffer to hold more than one key when True
def enable_key_buffer(bool):
    global _key_buffer_en 
    _key_buffer_en = bool

#Push a new key into the buffer
def add_to_buffer(char):
    global _key_buffer
    if (_key_buffer_en & (len(_key_buffer) != 0)):
        _key_buffer.append(char)
    else:
        _key_buffer = [char]

#Fetch the next key from the buffer, if there is no key in the buffer, then return nothing
def fetch_next():
    #Check if there is a key in the buffer
    if len(_key_buffer) > 0:
        #Pop first entry in buffer
        return _key_buffer.pop(0)
    else:
        #Return nothing
        return

#Enable a different keyset to be used when a button is held for longer when True
def enable_long_press_event(bool):
    global _long_press_en 
    _long_press_en = bool


#Main function
#-----------------------------------------------
#Dispose of this when done. Shouldn't be part of library, its only for testing

if __name__ == "__main__":
    try:
        initialize_gpio(long_press_en=True,key_buffer_en=True)
        while True:
            if len(_key_buffer) < 3:
                pass
                
            else:
                print(_key_buffer)
                print(fetch_next())
                print(fetch_next())
                print(fetch_next())

    
    except Exception as e:
        print(e) 
