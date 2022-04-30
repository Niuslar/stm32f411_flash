# STM32F411xx Programmer 

This script uses a Raspberry Pi to download a .bin file into a STMF411xx MCU. 

To use it, make the following connections: 

   RPi   |    STM32F411xx
--------------------------
  PIN 3  |   BOOT0 
  PIN 5  |   PB2 (BOOT1)
  PIN 6  |   GND 
  PIN 8  |   PA10 (RX)
  PIN 10 |   PA9  (TX)
  PIN 11 |   NRST

  # Using the script 

  To use the script, simply add the path to the .bin file when executing it. 
  ### Example:
  ```
  ./stm32f411_flasher.py blink_led.bin
  ```

  
