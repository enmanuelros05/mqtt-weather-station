import paho.mqtt.client as mqtt
import datetime

# CONFIGURACIÓN MQTT
SERVIDOR = "mqtt.eict.ce.pucmm.edu.do"
PUERTO = 1883
USUARIO = "itt363-grupo3"
PASSWORD = "CnFebqnjbq7F"

# TÓPICO DE SUSCRIPCIÓN (WILDCARD)
RUTA_PRINCIPAL = "/itt363-grupo3/estacion/#"


# CALLBACKS DE EVENTOS

def conexion_exitosa(mi_cliente, userdata, flags, reason_code, properties):
    # En CallbackAPIVersion.VERSION2, reason_code = 0 indica éxito de conexión
    if reason_code == 0:
        print(">>> Conectado al servidor MQTT <<<")
        print(f"Escuchando en: {RUTA_PRINCIPAL}\n")
        mi_cliente.subscribe(RUTA_PRINCIPAL)
    else:
        print(f"Error en la conexión. Código de retorno: {reason_code}")


def recibir_datos(mi_cliente, userdata, msg):
    # Separar la ruta del tópico para extraer estación y sensor
    partes = msg.topic.split('/')
    
    # La estructura esperada tiene 6 partes (ej: ['', 'itt363-grupo3', 'estacion', 'ID', 'sensores', 'nombre'])
    if len(partes) >= 6:
        nombre_estacion = partes[3]
        tipo_sensor = partes[5]
        dato = msg.payload.decode('utf-8')
        hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("-" * 40)
        print(f"Hora: {hora_actual}")
        print(f"Estación: {nombre_estacion.replace('-', ' ').title()}")
        print(f"Sensor: {tipo_sensor.replace('-', ' ').title()}")
        print(f"Lectura: {dato}")
        print("-" * 40 + "\n")
    else:
        # Manejar tópicos con estructuras diferentes que caigan en el wildcard
        print(f"Formato no reconocido en: {msg.topic}")
        print(f"Contenido: {msg.payload.decode('utf-8')}\n")


# CREAR CLIENTE MQTT
mi_cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mi_cliente.username_pw_set(USUARIO, PASSWORD)

mi_cliente.on_connect = conexion_exitosa
mi_cliente.on_message = recibir_datos

# CONECTARSE AL BROKER
print(f"Conectando a {SERVIDOR}...")
try:
    mi_cliente.connect(SERVIDOR, PUERTO, 60)
except Exception as e:
    print(f"Fallo al conectar: {e}")
    exit(1)

# BUCLE DE ESCUCHA CONTINUA
try:
    print("Monitor iniciado. Presiona Ctrl+C para detener.")
    mi_cliente.loop_forever()
except KeyboardInterrupt:
    print("\nCerrando conexión...")
    mi_cliente.disconnect()
    print("Adiós.")

