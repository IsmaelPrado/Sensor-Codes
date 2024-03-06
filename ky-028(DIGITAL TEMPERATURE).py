import network
from time import sleep
from umqtt.simple import MQTTClient
from machine import Pin, ADC

MQTT_BROKER = "172.20.10.6"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/ky-028"
MQTT_PORT = 1883

SENSOR_ANALOG_PIN = 35  # Pin analógico al que está conectado el sensor KY-082
SENSOR_DIGITAL_PIN = 2  # Pin digital al que está conectado el sensor KY-082

def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Conectando al WiFi", end="")
    sta_if.connect("ElGerasxd", "xdpapi23")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("WiFi conectado")

def llegada_mensaje(topic, msg):
    print(msg)

def subscribe():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.set_callback(llegada_mensaje)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a %s, suscrito al tema %s" % (MQTT_BROKER, MQTT_TOPIC))
    return client

wifi_connect()
client = subscribe()

# Configura el pin del sensor como una entrada analógica
sensor_pin_analog = ADC(Pin(SENSOR_ANALOG_PIN))
sensor_pin_analog.atten(ADC.ATTN_11DB)  # Rango de voltaje de 0-3.6V

# Configura el pin del sensor como una entrada digital
sensor_pin_digital = Pin(SENSOR_DIGITAL_PIN, Pin.IN)

while True:
    # Lee el valor analógico del sensor
    sensor_value_analog = sensor_pin_analog.read()

    # Lee el valor digital del sensor
    sensor_value_digital = sensor_pin_digital.value()

    # Publica los valores del sensor en el tema MQTT
    client.publish(MQTT_TOPIC + "/analog", str(sensor_value_analog))
    client.publish(MQTT_TOPIC + "/digital", str(sensor_value_digital))

    # Espera un tiempo antes de tomar otra lectura
    sleep(30)
 