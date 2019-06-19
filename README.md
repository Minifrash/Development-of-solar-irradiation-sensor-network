# Development of solar irradiation sensor network
The project approaches this goal by developing and deploying a sensor network, which nodes are designed as extension boards for the LoPy board. Each node is autonomous (the extension board powers the LoPy from a battery and includes a charger for the battery that takes energy from a power solar panel) and has several sensors (temperature, humidity, solar radiation and GPS) whose values are read periodically and are sent via Lora. The samples are sent to a LoRa gateway that is responsible for communicating using MQTT protocol (Lightweight protocol commonly used in IoT, Internet of things, based on publish / subscribe), to an external server with MQTT broker previously configured to receive the publications and that allows that clients can subscribe to them. The server includes a MQTT client (ThingsBoard, IoT open-source platform that allows a rapid development, management and scaling of IoT projects) that is subscribed to these publications and allows the graphical representation of the received data providing a human friendly visual representation of the data.

## Structure of the project
- ***Solar Node Folder***
     It contains the different services that make up the software architecture of the solar node and their respective configuration files.

- ***Gateway Folder***
     Contains the code in json format implemented in the Node-RED tool used in the gateway to control the different messages received by the nodes.
     
## Contributing
Changes and improvements are more than welcome! Feel free to fork and open a pull request. Please if you can, please make sure the code fully works before sending the pull request, as that will help speed up the process.

## License
This code is licensed under the [GPL-3.0](https://github.com/Minifrash/Development-of-solar-irradiation-sensor-network/blob/master/LICENSE).
