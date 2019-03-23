# Development of solar irradiation sensor network

## Resumen

Este proyecto engloba la idea de desplegar una red de nodos solares, formados por varios sensores, que repartidos por una zona geográfica realicen la recogida de muestras de varias magnitudes físicas, siendo la irradiación solar la más importante de ellas en este proyecto.  

Los datos recogidos por los distintos nodos solares que conforman la red serán procesados por un sistema predictivo, que predecirá la radiación solar del área geográfica donde estén situados los nodos en un futuro próximo.
De manera más concreta, este trabajo se centra en el despliegue de la red de nodos solares y en la recogida de magnitudes físicas procedentes de los distintos sensores, para su posterior envío a un servidor a través de un gateway.
La red de nodos solares utiliza la tecnología LoRa para la comunicación entre los nodos y un gateway que les da salida a Internet. Dicho gateway utiliza el protocolo MQTT para la comunicación con el servidor utilizando un broker como intermediario.  

En el servidor se utiliza la plataforma ThingsBoard como cliente suscrito al broker MQTT, que permitirá almacenar y representar gráficamente los datos recibidos.

## Estructura del projecto

- ***Carpeta Nodo Solar***

    Contiene los distintos servicios que conforman la arquitectura software del nodo solar y sus respectivos ficheros de configuración.

- ***Carpeta Gateway***  
    Contiene el código en formato json implementado en la herramienta Node-RED utilizada en el gateway para el control de los distintos mensajes recibidos por los nodos.
