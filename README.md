# 🌦️ Simulación de Estaciones Meteorológicas - Protocolo MQTT y MySQL

Este proyecto implementa un sistema IoT simulado en Python que utiliza el protocolo MQTT para la transmisión de datos meteorológicos consolidados en tiempo real en formato JSON, y almacena las lecturas de forma estructurada y automatizada en una base de datos relacional MySQL.

---

## 📋 Características

*   **Publicador JSON**: Genera lecturas consolidadas para múltiples estaciones meteorológicas y las publica periódicamente agrupadas en un único objeto JSON.
*   **Suscriptor MySQL**: Escucha los mensajes JSON en tiempo real a través de un tópico comodín (`+`) y los almacena de forma segura en una base de datos MySQL mediante consultas SQL parametrizadas.
*   **API Paho-MQTT v2**: Implementado utilizando la API más reciente (`CallbackAPIVersion.VERSION2`) para garantizar compatibilidad futura.
*   **Cierre Seguro**: Manejo ordenado de desconexión en ambos scripts ante interrupciones de teclado (`Ctrl+C`).

---

## 🛠️ Parámetros de Conexión

### 1. Broker MQTT
*   **Servidor**: `mqtt.eict.ce.pucmm.edu.do`
*   **Puerto**: `1883`
*   **Usuario**: `itt363-grupo3`
*   **Contraseña**: `CnFebqnjbq7F`

### 2. Base de Datos MySQL (Configurable en `subscriber.py`)
*   **Host**: `localhost`
*   **Puerto**: `3306`
*   **Usuario**: `root`
*   **Contraseña**: `""` (vacio)
*   **Nombre de Base de Datos**: `estacion_meteorologica`

---

## 🗄️ Esquema de Base de Datos MySQL

Para inicializar la base de datos y la tabla necesarias para este proyecto, ejecuta el siguiente script SQL en tu servidor MySQL:

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

## 📡 Jerarquía de Tópicos y Formato de Mensajes

Los mensajes se publican utilizando la estructura consolidada:

$$\text{/itt363-grupo3/\{estacion-ID\}/lecturas}$$

### Ejemplo de Tópico
`/itt363-grupo3/estacion-1/lecturas`

### Formato de Mensaje JSON (Payload)
```json
{
    "temperatura": 28,
    "humedad": 75,
    "lluvia": 12,
    "velocidad_viento": 35,
    "direccion_viento": "Norte"
}
```

> [!NOTE]
> Para suscribirse a todas las estaciones simuladas de este grupo, el comodín de ruta utilizado es:
> `/itt363-grupo3/+/lecturas`

---

## 🚀 Instrucciones de Ejecución

### 1. Instalación de Dependencias

Se requiere Python 3.8+ instalado. Instala las librerías necesarias ejecutando:

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el Suscriptor (Subscriber)

El suscriptor debe iniciarse primero para conectarse tanto al broker MQTT como a la base de datos MySQL local:

```bash
python subscriber/subscriber.py
```

### 3. Ejecutar el Publicador (Publisher)

En otra terminal independiente, inicia el publicador para empezar a generar datos simulados:

```bash
python publisher/publisher.py
```
