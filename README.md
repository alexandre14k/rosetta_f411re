# rosetta_f411re
Mixed-signal test board is the key to the unknown.

## About
Provided firmware binary is loaded on the TARGET via STM32F411RE NUCLEO embedded bootloader.<br>
The firmware allows testers to use the STM32F411RE MCU peripherals via virtual com port VCP.<br>
A basic REPL-DISPATCHER allows natural control over the hardware.<br>
The VCP is connected to USART2 TX-RX pins.<br>
The VCP line configuration uses 115200 baud speed with 8N1 and no DTS/RTS.<br>
The board pins are picked so that peripherals can be used independently.<br>

## Overview
- USART2 is reserved to communicate with host via VCP<br>
- USART1 is used to communicate with outside devices<br>
- SPI1 is used to communicate with outside devices<br>
- IC21 is used to communicate with outside devices<br>
- TIMx-WAVE pins can be toggled periodically as CLOCK or PWM<br>
- FREE-GPIO pins can be set/cleared<br>
- ADC channels A0 to A6 can be polled one by one, all one shot and all in burst mode<br>
- REPL allows to backspace/delete chars in the serial prompt<br>
- User BTN (blue) allow to trigger statemachine LED PA5 blinking each 500ms

## Prerequisites
- Python version 3.12

## File tree
<img width="795" height="657" alt="image" src="https://github.com/user-attachments/assets/b0f5d6a1-0233-4fba-bce0-6b9d77fbab0a" />

## Custom serial library
<img width="795" height="933" alt="image" src="https://github.com/user-attachments/assets/84af58fc-aabc-432a-86a1-52463db8bb81" />

## Features
<img width="795" height="979" alt="image" src="https://github.com/user-attachments/assets/a705a6df-d75a-49c7-a89c-fed219713436" />

## Pinout
<img width="795" height="1071" alt="image" src="https://github.com/user-attachments/assets/49415054-f90b-4540-a3c2-deeb36679f3e" />


## License

This project is licensed under the BSD 3-Clause License - see the LICENSE
file for details.

Copyright (c) 2026 alexander14k28@gmail.com

See [LICENSE](LICENSE) for the license governing this project.
