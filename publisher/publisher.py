import paho.mqtt.client as mqtt
import random
import time
import json

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
    "Norte", "Sur", "Este", "Oeste",
    "Noreste", "Noroeste", "Sureste", "Suroeste"
]

# CREAR CLIENTE MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)

# CONECTARSE AL BROKER
try:
    client.connect(BROKER, PORT, 60)
    print(">>> Conectado al broker MQTT <<<")
    print("Iniciando simulación meteorológica...\n")
except Exception as e:
    print(f"Fallo al conectar al broker: {e}")
    exit(1)

# PUBLICACIÓN CONTINUA
try:
    while True:
        for station in stations:
            # Generar objeto JSON consolidado con lecturas
            payload = {
                "temperatura": random.randint(20, 35),
                "humedad": random.randint(40, 95),
                "lluvia": random.randint(0, 50),
                "velocidad_viento": random.randint(0, 80),
                "direccion_viento": random.choice(wind_directions)
            }

            topic = f"/itt363-grupo3/{station}/lecturas"
            
            # Publicar JSON serializado
            client.publish(topic, json.dumps(payload))
            
            print(f"[{station}] -> Publicado en {topic}:")
            print(json.dumps(payload, indent=4, ensure_ascii=False))
            print("-" * 50)

        time.sleep(5)

except KeyboardInterrupt:
    print("\nDeteniendo publicación y cerrando conexión...")
    client.disconnect()
    print("Adios.")
