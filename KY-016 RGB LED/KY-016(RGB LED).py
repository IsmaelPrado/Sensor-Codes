import network
from time import sleep
from umqtt.simple import MQTTClient
from machine import Pin, I2C
import ssd1306

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/rgb"
MQTT_PORT = 1883

# Configurar pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Pines SDA y SCL de la Raspberry Pi
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configurar pines del sensor RGB
pin_R = Pin(12, Pin.IN)
pin_G = Pin(13, Pin.IN)
pin_B = Pin(14, Pin.IN)

def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Connect", end="")
    sta_if.connect("ElGerasxd", "xdpapi23")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("Wifi connected")

def get_color():
    r = pin_R.value()
    g = pin_G.value()
    b = pin_B.value()
    if r == 1 and g == 0 and b == 0:
        return "ROJO"
    elif r == 0 and g == 1 and b == 0:
        return "VERDE"
    elif r == 0 and g == 0 and b == 1:
        return "AZUL"
    else:
        return "OTRO"

def oled_display(color):
    global oled
    oled.fill(0)
    oled.text("Color: " + color, 0, 0)
    oled.show()

def llegada_mensaje(topic, msg):
    print(msg)
    oled_display(msg.decode())
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

while True:
        color = get_color()
        oled_display(color)
        client.publish(MQTT_TOPIC, color)
        sleep(5)  # Espera 1 segundo antes de volver a leer el color
