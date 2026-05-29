import paho.mqtt.client as mqtt
import mysql.connector
import json
import datetime

# CONFIGURACIÓN MQTT
SERVIDOR = "mqtt.eict.ce.pucmm.edu.do"
PUERTO = 1883
USUARIO = "itt363-grupo3"
PASSWORD = "CnFebqnjbq7F"

# TÓPICO DE SUSCRIPCIÓN (WILDCARD)
RUTA_PRINCIPAL = "/itt363-grupo3/+/lecturas"

# CONFIGURACIÓN MYSQL
DB_HOST = "192.168.34.193"
DB_USER = "sistema"
DB_PASSWORD = "12345678"
DB_NAME = "estacion_meteorologica"


# CONEXIÓN Y ALMACENAMIENTO EN BASE DE DATOS

def guardar_lectura(id_estacion, datos):
    try:
        # Conectar temporalmente a la base de datos
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Extraer el ID numérico si la estación contiene números (ej: "estacion-3" -> 3)
        # Esto previene errores de "Incorrect integer value" si el campo en la BD es entero.
        import re
        match = re.search(r'\d+', id_estacion)
        id_estacion_db = int(match.group()) if match else id_estacion
        
        # Consulta parametrizada para inserción segura
        query = """
            INSERT INTO lectura (id_estacion, temperatura, humedad, lluvia, velocidad_viento, direccion_viento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            id_estacion_db,
            datos.get("temperatura"),
            datos.get("humedad"),
            datos.get("lluvia"),
            datos.get("velocidad_viento"),
            datos.get("direccion_viento")
        )
        
        cursor.execute(query, valores)
        conn.commit()
        print(f"[BD] Lectura de {id_estacion} almacenada correctamente en MySQL.")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"[BD ERROR] Fallo al guardar en base de datos para {id_estacion}: {err}")


# CALLBACKS DE EVENTOS MQTT

def conexion_exitosa(mi_cliente, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print(">>> Conectado al servidor MQTT <<<")
        print(f"Escuchando en: {RUTA_PRINCIPAL}\n")
        mi_cliente.subscribe(RUTA_PRINCIPAL)
    else:
        print(f"Error en la conexión MQTT. Código de retorno: {reason_code}")


def recibir_datos(mi_cliente, userdata, msg):
    partes = msg.topic.split('/')
    
    # Validar formato de tópico esperado: ['', 'itt363-grupo3', 'estacion-ID', 'lecturas']
    if len(partes) >= 4:
        id_estacion = partes[2]
        
        try:
            # Decodificar el payload JSON
            datos = json.loads(msg.payload.decode('utf-8'))
            
            # Imprimir confirmación en consola
            hora_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("-" * 50)
            print(f"Hora de recepción: {hora_actual}")
            print(f"Estación origen: {id_estacion}")
            print("Datos JSON recibidos:")
            print(json.dumps(datos, indent=4, ensure_ascii=False))
            
            # Almacenar en la base de datos
            guardar_lectura(id_estacion, datos)
            print("-" * 50 + "\n")
            
        except json.JSONDecodeError as err:
            print(f"[ERROR JSON] No se pudo analizar el payload como JSON: {err}")
        except Exception as err:
            print(f"[ERROR] Error inesperado procesando mensaje: {err}")
    else:
        print(f"Tópico no reconocido: {msg.topic}")


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
    print(f"Fallo al conectar al broker: {e}")
    exit(1)

# BUCLE DE ESCUCHA CONTINUA
try:
    print("Monitor iniciado (con soporte MySQL). Presiona Ctrl+C para detener.")
    mi_cliente.loop_forever()
except KeyboardInterrupt:
    print("\nCerrando conexión MQTT...")
    mi_cliente.disconnect()
    print("Adiós.")


