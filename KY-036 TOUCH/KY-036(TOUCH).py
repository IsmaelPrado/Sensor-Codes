from machine import Pin
from umqtt.simple import MQTTClient
import network
from time import sleep

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/touch"
MQTT_PORT = 1883

# Definimos el pin para el sensor táctil KY-036
TOUCH_SENSOR_PIN = 15  # Ajusta este pin según tu configuración

# Inicializamos el pin del sensor táctil como entrada
touch_sensor = Pin(TOUCH_SENSOR_PIN, Pin.IN, Pin.PULL_UP)

# Variable para almacenar el estado anterior del sensor táctil
previous_touch_state = touch_sensor.value()

def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Conectando", end="")
    sta_if.connect("ElGerasxd", "xdpapi23")  # Nombre y contraseña de tu red Wi-Fi
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
    touch_state = touch_sensor.value()  # Leer el estado actual del sensor táctil

    if touch_state != previous_touch_state:  # Verificar si el estado del sensor ha cambiado
        print("Estado del sensor táctil:", touch_state)
        client.publish(MQTT_TOPIC, str(touch_state))  # Enviar el estado del sensor al servidor MQTT
        previous_touch_state = touch_state  # Actualizar el estado anterior del sensor

    sleep(0.1)  # Pequeño retardo para evitar lecturas rápidas del sensor
