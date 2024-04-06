from machine import Pin
from umqtt.simple import MQTTClient
import network
from time import sleep

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/tilt"
MQTT_PORT = 1883

# Definimos el pin para el sensor de inclinación KY-017
TILT_SENSOR_PIN = 34  # Ajusta este pin según tu configuración

# Inicializamos el pin del sensor de inclinación como entrada
tilt_sensor = Pin(TILT_SENSOR_PIN, Pin.IN, Pin.PULL_UP)

# Variable para almacenar el estado anterior del sensor de inclinación
previous_tilt_state = tilt_sensor.value()

def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Conectando", end="")
    sta_if.connect("nombre_de_red", "contraseña")  # Nombre y contraseña de tu red Wi-Fi
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("Wi-Fi conectado")

def llegada_mensaje(topic, msg):
    print(msg)
    client.publish(MQTT_TOPIC, msg)

def subscribe():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, suscrito al tema %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

wifi_connect()
client = subscribe()

# Bucle principal
while True:
    tilt_state = tilt_sensor.value()  # Leer el estado actual del sensor de inclinación

    if tilt_state != previous_tilt_state:  # Verificar si el estado del sensor ha cambiado
        print("Estado del sensor de inclinación:", tilt_state)
        client.publish(MQTT_TOPIC, str(tilt_state))  # Enviar el estado del sensor al servidor MQTT
        previous_tilt_state = tilt_state  # Actualizar el estado anterior del sensor

    sleep(0.1)  # Pequeño retardo para evitar lecturas rápidas del sensor
