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
#Constants
#-----------------------------------------------

#Default Keysets
DEFAULT_SHORT_PRESS_KEYSET = ['1','2','3','4','5','6','7','8','9','*','0','#']
DEFAULT_LONG_PRESS_KEYSET = ['A','B','C','D','E','F','G','H','I','J','K','L']

#Default Pinsets
DEFAULT_COLUMN_PINSET = [11,13,15,19] 
DEFAULT_ROW_PINSET = [16,18,22,24]

#Default Timings
DEFAULT_BOUNCETIME = 300
DEFAULT_LONG_PRESS_DELAY = 500


#-----------------------------------------------
#Class Definition
#-----------------------------------------------

class EOZ_IP40:


#-----------------------------------------------
#Class Variables
#-----------------------------------------------
    
    #Buffers
    key_buffer = []		#Buffer containing a FIFO list of the pressed keys. When key_buffer_en is False, it can only store a single key
    
    #Keysets
    short_press_keyset = []	#The array of characters mapped to each key. The first entry is the top left key and progression goes from left to right, top to bottom
    long_press_keyset = []	#As above, but explicitly for long presses
    
    #Timings
    long_press_delay = []	#Time in milliseconds a button must be held to register as a long press

    #Pinsets
    column_pinset = []		#The GPIO pins associated with the columns. The first entry is the leftmost column and progression goes from left to right, last entry is a callback pin
    row_pinset = []		#The GPIO pins associated with the rows. The first entry is the topmost row and progression goes from top to bottom


#Flags
#-----------------------------------------------
    
    long_press_en = None	#Flag that indicates long presses are allowed when True
    key_buffer_en = None	#Flag that indicates more than one character is allowed to be stored in the buffer when True
    keypad_active = None	#Flag that indicates the keypad is active when True


#-----------------------------------------------
#Functions
#-----------------------------------------------
 
#GPIO Functions
#-----------------------------------------------

    #Initialize all the GPIO pins that the keypad uses and assign callbacks
    def initialize_gpio(self):
               
        #Set GPIO mode to board
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
    
        #Initialize column pins as input pins that are pulled down
        GPIO.setup(self.column_pinset, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
        #Initialize row pins as output pins with a default high logic value
        GPIO.setup(self.row_pinset, GPIO.OUT)
        GPIO.output(self.row_pinset, GPIO.HIGH)
    
        #Add interupt callback to column pins if requested
        if self.keypad_active == True:
            GPIO.add_event_detect(self.column_pinset[3], GPIO.RISING, bouncetime=DEFAULT_BOUNCETIME)
            GPIO.add_event_callback(self.column_pinset[3], self.press_event)
        
    #Clears all the GPIO pins that the keypad uses and unassigns callbacks will require a call of initialize_gpio for keypad to work again
    def cleanup_gpio(self):
        
        #Set GPIO mode to board
        GPIO.setmode(GPIO.BOARD)
        
        #Cleanup pins
        GPIO.cleanup(self.row_pinset)
        GPIO.cleanup(self.column_pinset)
    
    #Activates the callback funtion and sets the row pins to high
    def activate_keypad(self):
        
        #Set row pins to high
        GPIO.output(self.row_pinset, GPIO.HIGH)
        
        #Setup the callback event
        GPIO.add_event_detect(self.column_pinset[3], GPIO.RISING, bouncetime=DEFAULT_BOUNCETIME)
        GPIO.add_event_callback(self.column_pinset[3], self.press_event)
    
        #Set flags
        self.keypad_active = True
        
    #Deactivate the callback function and set the row pins to low
    def deactivate_keypad(self):
        
        #Set row pins to low
        GPIO.output(self.row_pinset, GPIO.LOW)

        #Stop the callback event
        GPIO.remove_event_detect(self.column_pinset[3])
    
        #Set flags
        self.keypad_active = False

    
#Callback Function
#-----------------------------------------------
    
    #Interupt function that triggers when a button is pressed while the keypad is active
    def press_event(self, channel):
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
            #Start long press timer, skip if long presses are disabled
            if self.long_press_en:
                press_start = timer()
    
            #Identify the colum pin that triggered the event
            for pin in self.column_pinset:
                if (pin != channel) & (GPIO.input(pin) == GPIO.HIGH):
                    column_pin = pin
                    break
        
            #Identify the row pin that triggered the event
            for pin in self.row_pinset:
                GPIO.output(pin, GPIO.LOW)
                if GPIO.input(column_pin) == GPIO.LOW:
                    row_pin = pin
                    GPIO.output(pin, GPIO.HIGH)
                    break                
    
            #Stop timer for long presses on falling edge and compare to long_press_delay, skip if long presses are disabled
            if self.long_press_en:
                GPIO.wait_for_edge(column_pin, GPIO.FALLING)
                press_end = timer()
                if (press_end - press_start)*1000 > self.long_press_delay:
                    long_press = True

            #Reset the row GPIO pins
            GPIO.output(self.row_pinset,GPIO.HIGH)
        
            #Get a pair of values that, when added together, map to the correct key
            column_value = None
            row_value = None
            if column_pin == self.column_pinset[0]:
                column_value = 0
            elif column_pin == self.column_pinset[1]:
                column_value = 1
            elif column_pin == self.column_pinset[2]:
                column_value = 2
            else:
                raise Exception("Invalid pin")

            if row_pin == self.row_pinset[0]:
                row_value = 0
            elif row_pin == self.row_pinset[1]:
                row_value = 3
            elif row_pin == self.row_pinset[2]:
                row_value = 6
            elif row_pin == self.row_pinset[3]:
                row_value = 9
            else:
                raise Exception("Invalid pin")

            #Choose the correct key buffer
            if long_press == True:
                self.add_to_buffer(self.long_press_keyset[row_value+column_value])
            else:
                self.add_to_buffer(self.short_press_keyset[row_value+column_value])     

        except Exception as e:
            print(e)
            #Reset the row GPIO pins
            GPIO.output(self.row_pinset, GPIO.HIGH)
         
    
#Key Buffer Functions
#-----------------------------------------------

    #Enable the key buffer to hold more than one key when True
    def enable_key_buffer(self, bool): 
        self.key_buffer_en = bool

    #Push a new key into the buffer
    def add_to_buffer(self, char):
        if (self.key_buffer_en & (len(self.key_buffer) != 0)):
            self.key_buffer.append(char)
        else:
            self.key_buffer = [char]

    #Fetch the next key from the buffer, if there is no key in the buffer, then return nothing
    def fetch_next(self):
        #Check if there is a key in the buffer
        if len(self.key_buffer) > 0:
            #Pop first entry in buffer
            return self.key_buffer.pop(0)
        else:
            #Return nothing
            return

    #Fetch all the keys currently in the buffer, if there are no keys in the buffer, then return nothing
    def fetch_all(self):
        #Check if there is a key in the buffer
        if len(self.key_buffer) > 0:
            #Transfer all keys to new array while emptying buffer
            output = []
            while len(self.key_buffer) > 0:
                output.append(self.key_buffer.pop(0))
            #Return array
            return output
        else:
            #Return nothing
            return


#Long Press Functions
#-----------------------------------------------

    #Enable a different keyset to be used when a button is held for longer when True
    def enable_long_press_event(self, bool): 
        self.long_press_en = bool


#Class Initialization Functions
#-----------------------------------------------

    #Constructor. Creates an object instances of this class.
    def __init__(self, column_pinset=DEFAULT_COLUMN_PINSET, row_pinset=DEFAULT_ROW_PINSET, short_press_keyset=DEFAULT_SHORT_PRESS_KEYSET, long_press_keyset=DEFAULT_LONG_PRESS_KEYSET, long_press_delay=DEFAULT_LONG_PRESS_DELAY, long_press_en=False, key_buffer_en=False, keypad_active=True):

        #Set all the class variables
        self.column_pinset = column_pinset
        self.row_pinset = row_pinset
        self.short_press_keyset = short_press_keyset
        self.long_press_keyset = long_press_keyset
        self.long_press_delay = long_press_delay
        self.long_press_en = long_press_en
        self.key_buffer_en = key_buffer_en
        self.keypad_active = keypad_active

        #Initialize GPIO
        self.initialize_gpio()
