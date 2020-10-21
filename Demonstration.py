import EOZ_IP40 as Keypad
import Lock_Pad as Lock
import RPi.GPIO as GPIO

if __name__ == "__main__":
    Keypad.initialize_gpio()
    Lock.initialize_gpio()
    while True:
        try:        
            x = input("Enter a 3 digit code to set the lock: ")
            if len(x) != 3:
                raise Exception("Incorrect number of characters")
            passcode = []
            for char in x:
                valid = False
                for key in Keypad._short_press_keyset:
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
    
    gpio.cleanup()