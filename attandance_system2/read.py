from pirc5221 import RFID
import signal
import time
import RPi.GPIO as GPIO
import DbOperations

rdr = RFID()
util = rdr.util()
util.debug = True
print("Cikis Servisi Hazır.Kart bekleniyor...")
continue_reading = True
latestCardId = ""
latestCardTimeCount = 0
closeTimeInterval = 2
latestCardStart = time.time()
successPinNumber = 38
successPinOpened = False
failPinNumber = 40
readerType = 1
# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(successPinNumber, GPIO.OUT)
GPIO.setup(failPinNumber, GPIO.OUT)
GPIO.setup(failPinNumber, GPIO.OUT)
# autheticated attempt - success
def successOpenPin():
    global successPinNumber
    global successPinOpened
    successPinOpened = True
    GPIO.output(successPinNumber,GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(successPinNumber,GPIO.HIGH)
    return
def successClosePin():
    global successPinNumber
    global successPinOpened
    successPinOpened = False
    GPIO.output(successPinNumber,GPIO.LOW)    
    return
# not autheticated attempt - fail
def failPin():
    global successPinNumber
    global successPinOpened
    global failPinNumber
    successPinOpened = False
    GPIO.output(successPinNumber,GPIO.LOW)

    GPIO.output(failPinNumber,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(failPinNumber,GPIO.LOW)
    return
try:
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    while continue_reading:
        currentTime = time.time()
        elapsedTime = currentTime - latestCardTimeCount
            
        if elapsedTime > 0.2 and successPinOpened == True:
            successClosePin()
        
        if elapsedTime > closeTimeInterval and successPinOpened == True:
            latestCardId = ""
            successClosePin()
            latestCardTimeCount = time.time()
        rdr.wait_for_tag()
        (error, data) = rdr.request()
        if not error:
         (error, uid) = rdr.anticoll()
         if not error:
               
            # Print UID
            part1 = str(hex(uid[3])[2:])
            part2 = str(hex(uid[2])[2:])
            part3 = str(hex(uid[1])[2:])
            part4 = str(hex(uid[0])[2:])
                
            if len(part1) == 1:
                part1 = "0" + part1
            if len(part2) == 1:
                part2 = "0" + part2
            if len(part3) == 1:
                part3 = "0" + part3
            if len(part4) == 1:
                part4 = "0" + part4
                
            bag_tag_str = str(part1 + part2 + part3 + part4)
            bag_tag = int(bag_tag_str, 16)
                
            tempCardId = bag_tag
            if tempCardId != latestCardId:
                latestCardTimeCount = time.time()
                latestCardId = tempCardId
                    
                if DbOperations.checkUserExist(latestCardId) == 1:
                    successOpenPin()
                    DbOperations.insertAuthorize(latestCardId, readerType, 1)
                else:
                    failPin()
                    DbOperations.insertAuthorize(latestCardId, readerType, 0)
                    
            else:
                currentTime = time.time()
                elapsedTime = currentTime - latestCardTimeCount
                if elapsedTime > closeTimeInterval:
                    latestCardTimeCount = time.time()
                    if DbOperations.checkUserExist(latestCardId) == 1:
                        successOpenPin()
                        DbOperations.insertAuthorize(latestCardId, readerType, 1)
                    else:
                        failPin()
                        DbOperations.insertAuthorize(latestCardId, readerType, 0)

finally:
    GPIO.cleanup()
