import EOZ_IP40 as Keypad
import Lock_Pad as Lock
import RPi.GPIO as GPIO        
    
def keyboard_mode():        
    try:        
        x = str(input("Enter a 3 digit code to set the lock: "))
        if len(x) != 3:
            raise Exception("Incorrect number of characters")
        passcode = []
        for char in x:
            valid = False
            for key in Keypad._short_press_keyset:
                if char == key:
                     passcode.append(char)
                     valid = True
            if Keypad._long_press_en == True:
                for key in Keypad._long_press_keyset:
                    if char == key:
                        passcode.append(char)
                        valid = True
            
            if valid == False:
                raise Exception("Character " + char + " is not in the keyset")
            
        print("The passcode is: " + x)
        Lock.close_lock()
        print("Lock engaged")
            
        key_inputs = []
        while True:
            t = Keypad.fetch_next()
            if t != None:
                key_inputs.append(t)
                print(t)
            if len(key_inputs) == 3:
                i = 0
                while i <3:
                    if key_inputs[i] != passcode[i]:
                        print("Incorrect password")
                        key_inputs = []
                        break
                    i += 1
                if i == 3:
                    print("Correct password")
                    Lock.open_lock()
                    print("Lock disengaged")
                    break                            
        
    except Exception as e:
        print(e)

def keypad_mode():
    try:
        passcode = []
        print("Enter a 3 digit code to set the lock: ")
        while True:
            x = Keypad.fetch_next()
            if x != None:
                passcode.append(x)
                print(x)
            if len(passcode) == 3:
                break
        print("The passcode is: "+ "".join(passcode))
        Lock.close_lock()
        print("Lock engaged")
        
        key_inputs = []
        while True:
            t = Keypad.fetch_next()
            if t != None:
                key_inputs.append(t)
                print(t)
            if len(key_inputs) == 3:
                i = 0
                while i <3:
                    if key_inputs[i] != passcode[i]:
                        print("Incorrect password")
                        key_inputs = []
                        break
                    i += 1
                if i == 3:
                    print("Correct password")
                    Lock.open_lock()
                    print("Lock disengaged")
                    break        
        
    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    Keypad.initialize_gpio()
    Lock.initialize_gpio()
    while True:
        y = Keypad.fetch_next()
        if y == None:
            pass
        elif y == '*':  #Exit
            break
        elif y == '1':  #Keyboard input
            keyboard_mode()
        elif y == '2':  #Keypad input
            keypad_mode()
        elif y == '3':  #Toggle long presses
            if Keypad._long_press_en == False:
                print("long press enabled")
                Keypad.enable_long_press_event(True)
            else:
                print("long press disabled")
                Keypad.enable_long_press_event(False)
        elif y == '4':  #Toggle lock
            if Lock._lock_open == True:
                Lock.close_lock()
            else:
                Lock.open_lock()
        elif y == '5':
            while True:
                x = Keypad.fetch_next()
                if x != None:
                    print(x)
                if x == '*':
                    break
    
    GPIO.cleanup()
