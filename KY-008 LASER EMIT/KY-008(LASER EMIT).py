from machine import Pin
from umqtt.simple import MQTTClient
import network
from time import sleep

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/laser"
MQTT_PORT = 1883

# Definimos los pines para el botón y el módulo KY-008 de emisión láser
LASER_PIN = 13  # Ajusta este pin según tu configuración
BUTTON_PIN = 14

# Inicializamos los pines
laser = Pin(LASER_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Variable para almacenar el estado anterior del botón
previous_button_state = button.value()

def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Connect", end="")
    sta_if.connect("ElGerasxd", "xdpapi23")  # Nombre y contraseña de tu red Wi-Fi
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("Wifi connected")

def llegada_mensaje(topic, msg):
    print(msg)
    client.publish(MQTT_TOPIC, msg)

def subscribe():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Connected to %s, subscribed to topic %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

wifi_connect()
client = subscribe()

# Función para encender el láser
def encender_laser():
    laser.value(1)  # Encender el láser
    print("Láser encendido")

# Función para apagar el láser
def apagar_laser():
    laser.value(0)  # Apagar el láser
    print("Láser apagado")

# Bucle principal
while True:
    button_value = button.value()  # Leer el valor actual del botón

    if button_value != previous_button_state:  # Verificar si el estado del botón ha cambiado
        print("Valor del botón:", button_value)
        client.publish(MQTT_TOPIC, button_value)  # Enviar el valor del botón al servidor MQTT
        previous_button_state = button_value  # Actualizar el estado anterior del botón

    if button_value == 0:  # Verificar si el botón está presionado (botón activado por pull-up)
        encender_laser()
    else:
        apagar_laser()

    sleep(0.1)  # Pequeño retardo para evitar la lectura rápida del botón
