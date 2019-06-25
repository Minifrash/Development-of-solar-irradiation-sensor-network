# Development of solar irradiation sensor network
The project approaches this goal by developing and deploying a sensor network, which nodes are designed as extension boards for the LoPy board. Each node is autonomous (the extension board powers the LoPy from a battery and includes a charger for the battery that takes energy from a power solar panel) and has several sensors (temperature, humidity, solar radiation and GPS) whose values are read periodically and are sent via Lora. The samples are sent to a LoRa gateway that is responsible for communicating using MQTT protocol (Lightweight protocol commonly used in IoT, Internet of things, based on publish / subscribe), to an external server with MQTT broker previously configured to receive the publications and that allows that clients can subscribe to them. The server includes a MQTT client (ThingsBoard, IoT open-source platform that allows a rapid development, management and scaling of IoT projects) that is subscribed to these publications and allows the graphical representation of the received data providing a human friendly visual representation of the data.

## Structure of the project
- ***Solar Node Folder***
     It contains the different services that make up the software architecture of the solar node and their respective configuration files.

- ***Gateway Folder***
     Contains the code in json format implemented in the Node-RED tool used in the gateway to control the different messages received by the nodes.

## Get and install SolarNode
- ### GET
```sh
$ git clone https://github.com/Minifrash/Development-of-solar-irradiation-sensor-network.git
```
- #### Requirements
It is necessary to use the "Froze Code" technique which consists of including your own modules in a MicroPhyton firmware version, thus allowing the use of RAM for dynamic loading. The process of installing the necessary tools in the Frozen Code process consists of creating a new directory (pycom or other) in the $HOME directory and executing the following commands:
```sh
$ sudo apt-get install gcc git wget make libncurses-dev flex bison gperf python python-pip python-setuptools python-serial python-cryptography python-future python-pyparsing (packages needed for the process)
$ mkdir pycom
$ cd pycom
$ git clone https://github.com/pycom/pycom-micropython-sigfox.git
$ git clone https://github.com/pycom/pycom-esp-idf.git
$ cd pycom-esp-idf
$ git submodule update –init
$ cd ..
$ wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
$ tar zxf xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
$ export PATH=$PATH:$HOME/pycom/xtensa-esp32-elf/bin
$ export IDF_PATH=~/pycom/pycom-esp-idf
$ cd pycom-micropython-sigfox
$ cd mpy-cross && make clean && make && cd ..
```
- ### Install using Froze Code
To include the code in the firmware of MycroPhyton you have to copy the code of the application in the $HOME/pycom/pycom-micropython-sigfox/esp32/frozen/Common, and then copy the main.py and the boot.py of the application in the $HOME/pycom/pycom-micropython-sigfox/esp32/frozen/Base/. Finally, we put the device in "bootloader" mode, open a terminal in the $HOME/pycom/pycom-micropython-sigfox/esp32 directory and execute the following commands:
```sh
$ make BOARD=LOPY clean
$ make BOARD=LOPY TARGET=boot
$ make BOARD=LOPY TARGET=app
$ make BOARD=LOPY ESPPORT=<Path of the device> flash
```

## Contributing
Changes and improvements are more than welcome! Feel free to fork and open a pull request. Please if you can, please make sure the code fully works before sending the pull request, as that will help speed up the process.

## License
This code is licensed under the [GPL-3.0](https://github.com/Minifrash/Development-of-solar-irradiation-sensor-network/blob/master/LICENSE).
