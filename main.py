import paho.mqtt.client as mqtt
import mysql.connector
import json

# --- Configuración de MySQL ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "juan79-123",
    "database": "bdsensores"
}

# --- Configuración de MQTT ---
mqtt_server = "broker.hivemq.com"
topic_data = "sensores/datos_completos" # <-- Nos suscribimos a un solo tópico

# Función para la conexión a MySQL
def connect_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        return None

# Función que se ejecuta cuando el cliente se conecta al broker
def on_connect(client, userdata, flags, rc):
    print(f"Conectado al broker MQTT con código de resultado: {rc}")
    client.subscribe(topic_data)
    print(f"Suscrito al tópico: {topic_data}")

# Función que se ejecuta cuando llega un nuevo mensaje
def on_message(client, userdata, msg):
    try:
        # Decodifica el JSON del mensaje
        data_str = msg.payload.decode("utf-8")
        data = json.loads(data_str)
        
        temperatura = data.get("temperatura")
        humedad = data.get("humedad")
        presion = data.get("presion")

        conn = connect_db()
        if not conn:
            return

        cursor = conn.cursor()
        
        # Inserta todos los datos en una sola consulta
        query = "INSERT INTO lecturas_sensores (temperatura, humedad, presion) VALUES (%s, %s, %s)"
        cursor.execute(query, (temperatura, humedad, presion))
            
        conn.commit()
        print(f"Datos insertados en MySQL, temp: {temperatura}, hum: {humedad}, pres: {presion}.")
        cursor.close()
        conn.close()

    except json.JSONDecodeError:
        print("Error: El mensaje no es un JSON válido.")
    except Exception as e:
        print(f"Error general: {e}")

# Configura y arranca el cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(mqtt_server, 1883, 60)
    client.loop_forever()
except Exception as e:
    print(f"Error en la conexión MQTT: {e}")