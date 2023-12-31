## Carboardbot

### Usage: 
- Connect phone or laptop to "ESP_XXXX" wireless network, where XXXX is the ID of the robot
- Go to 192.168.4.1. 
- A webpage with four buttons should appear. Click them to move the robot.

### Installation: 
- In Arduino, go to Tools > ESP8266 Sketch Data Upload to upload the files from ./data to the ESP
- Then, in Arduino, compile and upload sketch to the ESP

### Requirements:
#### Arduino support for ESP8266 board
- In Arduino, add URL to Files > Preferences > Additional Board Managers URL.
- See https://learn.sparkfun.com/tutorials/esp8266-thing-hookup-guide/installing-the-esp8266-arduino-addon

#### Websockets library
- To install, Sketch > Include Library > Manage Libraries... > Websockets > Install
- https://github.com/Links2004/arduinoWebSockets


### Hardware: 
- NodeMCU Amica DevKit Board (ESP8266 chip)
- Motorshield for NodeMCU
- 2 continuous rotation servos plugged into motorshield pins D1, D2
- 1 Lipo Battery 3.8V 
- cardboard chassis
