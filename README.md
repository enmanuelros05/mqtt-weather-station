# Simulación de Estaciones Meteorológicas - Protocolo MQTT
Este proyecto implementa un sistema IoT simulado en Python que utiliza el protocolo MQTT para la transmisión de datos meteorológicos en tiempo real. Está configurado para conectarse al broker público de la PUCMM y simular múltiples estaciones con diversos sensores utilizando una jerarquía de tópicos organizada.

## Características
*   **Publicador Independiente**: Simula múltiples estaciones meteorológicas generando lecturas aleatorias de sensores de manera continua.
*   **Suscriptor Wildcard**: Escucha en tiempo real todas las publicaciones hechas en los canales de las estaciones a través de un único canal comodín (`#`).
*   **Compatibilidad Moderna**: Desarrollado utilizando la versión 2.x del API de callbacks de `paho-mqtt`.
*   **Robustez**: Ambos scripts manejan cierres limpios del sistema mediante señales de teclado (`Ctrl+C`), liberando correctamente los recursos y desconectándose del broker.

## Credenciales y Configuración del Broker
El sistema utiliza los siguientes parámetros para establecer conexión:

Broker/Servidor: mqtt.eict.ce.pucmm.edu.do
Puerto: 1883
Usuario: itt363-grupo3
Contraseña CnFebqnjbq7F

## Estructura y Jerarquía de Tópicos
Los tópicos utilizados siguen la estructura estándar solicitada:

$$\text{/itt363-grupo3/estacion/\{ID-estacion\}/sensores/\{nombre-sensor\}}$$

### Estaciones Simuladas
*   `estacion-1`
*   `estacion-2`
*   `estacion-3`

### Sensores Simulados por Estación
1.  `temperatura` (ºC)
2.  `humedad` (%)
3.  `lluvia` (mm)
4.  `viento` (Intensidad de 0 a 100)
5.  `velocidad-viento` (km/h)
6.  `direccion-viento` (Norte, Sur, Este, Oeste, etc.)

### Ejecutar el Subscriber
Para monitorear las lecturas que se envían al broker en tiempo real, inicia el suscriptor en una terminal:

```bash
python subscriber/subscriber.py
```

### Ejecutar el Publisher
Para iniciar la simulación y comenzar a publicar datos al broker, ejecuta el publicador en una segunda terminal separada:

```bash
python publisher/publisher.py
```
