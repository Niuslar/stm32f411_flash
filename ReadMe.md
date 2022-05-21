# STM32F411xx Programmer 

This script uses a Raspberry Pi to download a .bin file into a STMF411xx MCU. 

To use it, make the following connections: 


|   R-Pi  | STM32F411xx   |
| ------  | ------------- |
|  PIN 3  | BOOT0         |
|  PIN 4  | E5V*          |
|  PIN 5  | PB2 (BOOT1)   |
|  PIN 6  | GND           |
|  PIN 7  | NRST          |
|  PIN 8  | PA10 (RX)**   |
|  PIN 10 | PA9  (TX)**   |
[Raspberry Pi Pinout reference](https://linuxhint.com/wp-content/uploads/2022/02/gpio-pinout-raspberry-pi-01.png)

*I used a Nucleo-64 which has a pin to power the board with 5V (E5V). To use E5V, JP5 needs to be in the correct position (Table 8 of [UM1724](https://www.st.com/resource/en/user_manual/dm00105823-stm32-nucleo64-boards-mb1136-stmicroelectronics.pdf)).

**This is using USART1, other USART Pins could be used. Check [Application Note AN2606](https://www.st.com/resource/en/application_note/cd00167594-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf)

  ## Using the script 
  Add the path to the .bin file after the script name.
  ### Example:
  ```
  python3 stm32_flash_loader.py blink_led.bin
  ```
  
  ## Notes: 
  UART Must be enabled on the Raspberry Pi to use this script and it MUST use /dev/ttyAMA0. 
  /dev/ttyS0 or /dev/serial0 do not support even parity check very well, which is needed for the bootloader. 

  
