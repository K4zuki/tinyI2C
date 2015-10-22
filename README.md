tinyI2C
=======

## What is this?
This is a tiny UART-I2C converter project using mbed microcontrollers.
The module converts UART command packets into I2C/SPI protocol or GPIO to read/write with
configurable pull-up/pull-down modes.

- the "FTDI" USB-UART cable to connect to host PC; from PC the module look only an USB-Serial port
  - up to 115200 boudrate UART port to communicate
- up to 4 channel I2C ports with selectable speed
- one SPI port with 8/16 bits word, also selectable speed
- up to 2 x 8bit, General purpose IO ports

- tinyI2C       <-- root  
  - gui       <-- PyQt4 based GUI source codes  
  - mbed      <-- mbed source codes  
  - pcb       <-- PCB design files for eagle  
  - python    <-- python module code with standalone test program  

## Demo
  try `python/tinyI2C.py`

## Requirement
- Python 2.7  
  `apt-get install python`
- PySerial  
  `pip install pyserial`
* mbed microcontrollers using LPC824(recommended)/LPC1768/LPC11U24/LPC11U35  
  see [mbed.org](developer.mbed.org)

## Usage
1. write mbed program into your mbed
2. connect mbed to PC via Serial port
3. start gui software
4. select Serial port from dropdown list
5. you will be able to use up to 4 channels of I2C slaves and more!
    * check PinOut for your usage! ![](TinyI2C_PinOut.png)

## Install
1. install python 2.7 on your PC
2. install PySerial
3. (Windows only) if you use LpcXpresso 824 then install [mbed Serial port driver](http://developer.mbed.org/handbook/Windows-serial-configuration)

## Contribution by
Kazuki Yamamoto ( <k.yamamoto.08136891@gmail.com> )

## License
- [CC-BY-SA] (http://creativecommons.org/licenses/by-sa/4.0/legalcode)
- [CC-BY-SA 日本語](http://creativecommons.org/licenses/by-sa/2.1/jp/legalcode)

## Author

[K4zuki](https://github.com/K4zuki)
