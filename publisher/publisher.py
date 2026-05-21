import paho.mqtt.client as mqtt
import random
import time

# CONFIGURACIÓN MQTT
BROKER = "mqtt.eict.ce.pucmm.edu.do"
PORT = 1883

USERNAME = "itt363-grupo3"
PASSWORD = "CnFebqnjbq7F"

# ESTACIONES METEOROLÓGICAS
stations = [
    "estacion-1",
    "estacion-2",
    "estacion-3"
]


# DIRECCIONES DEL VIENTO
wind_directions = [
    "Norte",
    "Sur",
    "Este",
    "Oeste",
    "Noreste",
    "Noroeste",
    "Sureste",
    "Suroeste"
]

# CREAR CLIENTE MQTT
client = mqtt.Client()

# Configurar usuario y contraseña
client.username_pw_set(USERNAME, PASSWORD)

# Conectarse al broker
client.connect(BROKER, PORT, 60)

print("Conectado al broker MQTT")
print("Iniciando simulación meteorológica...\n")

# PUBLICACIÓN CONTINUA
while True:

    # Recorrer todas las estaciones
    for station in stations:

        # GENERAR DATOS ALEATORIOS
        temperatura = random.randint(20, 35)
        humedad = random.randint(40, 95)

        # Intensidad general del viento
        viento = random.randint(0, 100)

        lluvia = random.randint(0, 50)

        velocidad_viento = random.randint(0, 80)

        direccion_viento = random.choice(wind_directions)

        # CREAR DICCIONARIO DE SENSORES
        sensors = {
            "temperatura": temperatura,
            "humedad": humedad,
            "viento": viento,
            "lluvia": lluvia,
            "velocidad-viento": velocidad_viento,
            "direccion-viento": direccion_viento
        }

        # PUBLICAR CADA SENSOR
        for sensor, value in sensors.items():

            topic = f"/itt363-grupo3/estacion/{station}/sensores/{sensor}"

            client.publish(topic, value)

            print(f"[{station}]")
            print(f"Topic: {topic}")
            print(f"Valor: {value}")
            print("-" * 50)

    # Esperar antes de volver a publicar
    time.sleep(5)