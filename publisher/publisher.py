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
            # Generar lecturas de sensores
            temperatura = random.randint(20, 35)
            humedad = random.randint(40, 95)
            viento = random.randint(0, 100)
            lluvia = random.randint(0, 50)
            velocidad_viento = random.randint(0, 80)
            direccion_viento = random.choice(wind_directions)

            sensors = {
                "temperatura": temperatura,
                "humedad": humedad,
                "viento": viento,
                "lluvia": lluvia,
                "velocidad-viento": velocidad_viento,
                "direccion-viento": direccion_viento
            }

            # Publicar lectura de cada sensor
            for sensor, value in sensors.items():
                topic = f"/itt363-grupo3/estacion/{station}/sensores/{sensor}"
                client.publish(topic, value)
                
                print(f"[{station}] -> {sensor}: {value}")
            print("-" * 40)

        time.sleep(5)

except KeyboardInterrupt:
    print("\nDeteniendo publicación y cerrando conexión...")
    client.disconnect()
    print("Adios.")