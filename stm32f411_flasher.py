#!/usr/bin/env python3

from elftools.elf.elffile import ELFFile
from glob import glob
from time import sleep
from tracemalloc import start
import RPi.GPIO as GPIO
import serial
import sys

# RPi GPIO Pins used for flashing
LED = 7
BOOT0 = 3
BOOT1 = 5
RESET = 11

# Bootloader commands
uart_select_command = b'\x7F'

get_version = bytearray()
get_version.append(0x00)
get_version.append(0xFF)

get_version_and_read_ps = bytearray()
get_version_and_read_ps.append(0x01)
get_version_and_read_ps.append(0xFE)

get_id = bytearray()
get_id.append(0x02)
get_id.append(0xFD)

read_memory = bytearray()
read_memory.append(0x11)
read_memory.append(0xEE)

write_memory = bytearray()
write_memory.append(0x31)
write_memory.append(0xCE)

erase_memory = bytearray()
erase_memory.append(0x44)
erase_memory.append(0xBB)

global_erase = bytes.fromhex('ffff')

read_unprotect = bytearray()
read_unprotect.append(0x92)
read_unprotect.append(0x6D)

read_protect = bytearray()
read_protect.append(0x82)
read_protect.append(0x7D)

# Flash memory address
flash_add = bytearray()
flash_add.append(0x08)
flash_add.append(0x00)
flash_add.append(0x00)
flash_add.append(0x00)

ACK_BYTE = 0x79
NACK_BYTE = 0x1F

#Setup serial comm
ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=10) 

def setupPeripherals():      
    # Setup RPi GPIOs
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(LED,GPIO.OUT)
    GPIO.setup(BOOT0,GPIO.OUT)
    GPIO.setup(BOOT1,GPIO.OUT)
    GPIO.setup(RESET,GPIO.OUT)

def beginFlash():
    # Setup STM32 Bootloader 
    print('Activating STM32F411 Bootloader')
    GPIO.output(BOOT0,GPIO.HIGH)
    GPIO.output(BOOT1,GPIO.LOW)

    # Reset STM32
    GPIO.output(RESET,GPIO.LOW)
    sleep(0.1)
    GPIO.output(RESET,GPIO.HIGH)
    sleep(1)


# Send commands 
def startCommands():
    b_success = False
    ser.write(uart_select_command)
    response_byte = ser.read()
    if int(response_byte.hex(),16) == ACK_BYTE: 
        print("UART Recognised, ready to erase FLASH")
        b_success = True
    return b_success

def eraseMemory():
    b_success = False
    ser.write(erase_memory)
    response_byte = ser.read()
    if int(response_byte.hex(),16) == ACK_BYTE: 
        ser.write(global_erase)
        ser.write(b'\x00') # Checksum for global erase command
        response_byte = ser.read()
        if int(response_byte.hex(),16) == ACK_BYTE:
            print("FLASH successfuly erased")
            b_success = True
    if b_success == False:
        print("Error erasing FLASH")
    return b_success

def __printSectionInfo (s):
    print ('[{nr}] {name} {type} {addr} {offs} {size}'.format(
                nr = s.header['sh_name'],
                name = s.name,
                type = s.header['sh_type'],
                addr = s.header['sh_addr'],
                offs = s.header['sh_offset'],
                size = s.header['sh_size']
    ))

def processFile(filename):
    print('In file: ' + filename)
    with open(filename, 'rb') as f:
        # get the data
        elffile = ELFFile(f)
        print ('sections:')
        for s in elffile.iter_sections():
            __printSectionInfo(s)
        print ('Downloading .elf file to STM32')
        

def writeFlash(number_of_bytes):
    b_success = False
    bytes = hex(number_of_bytes)
    ser.write(write_memory)
    response_byte = ser.read()
    if int(response_byte.hex(),16) == ACK_BYTE:
        ser.write(flash_add)
        ser.write(0x08)    #checksum?
        if int(response_byte.hex(),16) == ACK_BYTE:
            ser.write(bytes)
    return b_success

def endFlash():
    # Restart board
    print('Reseting STM32 Board')
    GPIO.output(BOOT0, GPIO.LOW)
    GPIO.output(RESET, GPIO.LOW)
    sleep(0.1)
    GPIO.output(RESET,GPIO.HIGH)

    # Finishing routine
    GPIO.cleanup()
    ser.close()

def main():
    filename = sys.argv[-1]
    setupPeripherals()
    beginFlash()
    processFile(str(filename))
    #if startCommands() == True:
        #if eraseMemory() == True:
            #print("Finished")
            #endFlash()


if __name__ == "__main__":
    main()