# Simulación de Estaciones Meteorológicas - Protocolo MQTT y MySQL

Este proyecto contiene un publicador y un suscriptor desarrollados en Python. Simula el envío de datos meteorológicos a través del protocolo MQTT usando tramas JSON y almacena la información recibida en una base de datos MySQL.

---

## Estructura del Proyecto

*   **publisher/publisher.py**: Genera datos aleatorios de sensores para tres estaciones meteorológicas y los envía agrupados en un JSON.
*   **subscriber/subscriber.py**: Se conecta al broker MQTT, recibe los datos y los inserta en la base de datos MySQL.

---

## Configuración de Conexión

### 1. Broker MQTT
*   **Servidor**: `mqtt.eict.ce.pucmm.edu.do`
*   **Puerto**: `1883`
*   **Usuario**: `itt363-grupo3`
*   **Contraseña**: `CnFebqnjbq7F`

### 2. Base de Datos MySQL
*   **Host**: `localhost` (o la IP del servidor Linux)
*   **Puerto**: `3306`
*   **Usuario**: `root` (o el usuario configurado)
*   **Contraseña**: `""` (o la contraseña del usuario)
*   **Nombre de Base de Datos**: `estacion_meteorologica`

---

## Esquema de la Base de Datos

Script SQL para crear la base de datos y la tabla en el servidor MySQL:

```sql
CREATE DATABASE IF NOT EXISTS estacion_meteorologica;
USE estacion_meteorologica;

CREATE TABLE IF NOT EXISTS lectura (
    id_lectura INT AUTO_INCREMENT PRIMARY KEY,
    id_estacion VARCHAR(50) NOT NULL,
    temperatura INT,
    humedad INT,
    lluvia INT,
    velocidad_viento INT,
    direccion_viento VARCHAR(20),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Tópicos y Formato de Mensajes

El publicador envía los datos al siguiente tópico:
`/itt363-grupo3/estacion-ID/lecturas` (ejemplo: `/itt363-grupo3/estacion-1/lecturas`)

El suscriptor escucha usando el tópico wildcard:
`/itt363-grupo3/+/lecturas`

### Formato de Mensaje JSON
```json
{
    "temperatura": 28,
    "humedad": 75,
    "lluvia": 12,
    "velocidad_viento": 35,
    "direccion_viento": "Norte"
}
```

---

## Instrucciones para ejecutar

### 1. Instalación de dependencias
Ejecuta el siguiente comando para instalar las librerías necesarias:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el Suscriptor
Corre el suscriptor primero para que esté a la escucha y conectado a la base de datos:

```bash
python subscriber/subscriber.py
```

### 3. Ejecutar el Publicador
En otra terminal, corre el publicador para empezar a enviar los datos de las estaciones:

```bash
python publisher/publisher.py
```
