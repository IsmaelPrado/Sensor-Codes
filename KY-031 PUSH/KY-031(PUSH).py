import network
from umqtt.simple import MQTTClient
from machine import Pin, I2C
import ssd1306
import time  # Agregar la importación de time

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/ky-031"  # Cambio en el nombre del tema MQTT
MQTT_PORT = 1883

# Configurar pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Pines SDA y SCL de la Raspberry Pi
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

# Configurar pin del sensor KY-031
pin_sensor = Pin(5, Pin.IN)  # Cambio en el pin del sensor
last_sensor_value = None  # Variable para almacenar el último valor del sensor

def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Connect", end="")
    sta_if.connect("ElGerasxd", "xdpapi23")
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)  # Modificar para usar time.sleep()
    print("Wifi connected")

def get_sensor_value():
    return pin_sensor.value()  # Leer el valor del sensor KY-031

def oled_display(value):
    global oled
    oled.fill(0)
    oled.text("Sensor value: " + str(value), 0, 0)
    oled.show()

wifi_connect()

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
client.connect()

while True:
    sensor_value = get_sensor_value()
    
    if sensor_value != last_sensor_value:  # Si hay un cambio en el valor del sensor
        print("Sensor value:", sensor_value)  # Imprimir el nuevo valor del sensor en la consola
        oled_display(sensor_value)  # Mostrar el nuevo valor del sensor en la pantalla OLED
        client.publish(MQTT_TOPIC, str(sensor_value))  # Publicar el nuevo valor del sensor en el broker MQTT
        last_sensor_value = sensor_value  # Actualizar el último valor del sensor
    
    time.sleep(0.1)  # Esperar un momento antes de volver a leer el sensor y verificar si hay cambios