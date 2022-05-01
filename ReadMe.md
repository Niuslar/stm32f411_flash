# STM32F411xx Programmer 

This script uses a Raspberry Pi to download a .bin file into a STMF411xx MCU. 

To use it, make the following connections: 


|   R-Pi  | STM32F411xx   |
| ------  | ------------- |
|  PIN 2  | E5V*          |
|  PIN 3  | BOOT0         |
|  PIN 5  | PB2 (BOOT1)   |
|  PIN 6  | GND           |
|  PIN 7  | PA5 (LED)*    |  
|  PIN 8  | PA10 (RX)**   |
|  PIN 10 | PA9  (TX)**   |
|  PIN 11 | NRST          |
[Raspberry Pi Pinout reference](https://linuxhint.com/wp-content/uploads/2022/02/gpio-pinout-raspberry-pi-01.png)

*I used a Nucleo-64 board and used the E5V pin to power it. JP5 needs to be in the correct position to use this pin. 

*This is using USART1, other USART Pins could be used. Check [Application Note AN2606](https://www.st.com/resource/en/application_note/cd00167594-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf)

  ## Using the script 
  Add the path to the .bin file after the script name.
  ### Example:
  ```
  ./stm32f411_flasher.py blink_led.bin
  ```
  
  ## Notes: 
  UART Must be enabled on the Raspberry Pi to use this script and it MUST use /dev/ttyAMA0. 
  /dev/ttyS0 or /dev/serial0 do not support even parity check very well, which is needed for the bootloader. 

  
