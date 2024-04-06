from machine import Pin, I2C
from umqtt.simple import MQTTClient
import network
from time import sleep
import ssd1306
import dht  # Esta es la biblioteca para el sensor de temperatura y humedad

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/humidity"  # Cambiado a "sensor/humidity"
MQTT_PORT = 1883

# Configuración del display OLED
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Definimos el pin para el sensor de temperatura y humedad KY-015
TEMP_SENSOR_PIN = 15  # Ajusta este pin según tu configuración

# Inicializamos el sensor de temperatura y humedad
dht_sensor = dht.DHT11(Pin(TEMP_SENSOR_PIN))

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

def display_humidity(humidity):  # Cambiado a display_humidity
    oled.fill(0)
    oled.text("Humedad (%):", 0, 0, 1)  # Cambiado a "Humedad (%)"
    oled.text(str(humidity), 0, 20, 1)
    oled.show()

wifi_connect()
client = subscribe()

# Bucle principal
while True:
    dht_sensor.measure()  # Realizar la lectura del sensor de temperatura y humedad

    # Leer la humedad
    humidity = dht_sensor.humidity()  # Cambiado a humidity

    # Verificar si la humedad es válida (no es None)
    if humidity is not None:
        print("Humedad actual:", humidity)  # Cambiado a "Humedad actual:"
        client.publish(MQTT_TOPIC, str(humidity))  # Enviar la humedad al servidor MQTT
        display_humidity(humidity)  # Cambiado a display_humidity
    else:
        print("Error al leer el sensor DHT11")

    sleep(10)  # Esperar 10 segundos antes de la próxima lectura
