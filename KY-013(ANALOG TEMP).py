from machine import Pin, ADC, I2C
from umqtt.simple import MQTTClient
from time import sleep
import ssd1306

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/temperature"
MQTT_PORT = 1883

# Configurar ADC para el sensor de temperatura
adc = ADC(Pin(36))
adc.atten(ADC.ATTN_11DB)  # Configuración de atenuación para voltajes de 0-3.6V

# Configurar pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def wifi_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Conectando al WiFi...", end="")
    sta_if.connect("nombre_de_red", "contraseña_de_red")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.5)
    print("\nConexión WiFi exitosa:", sta_if.ifconfig())
    return sta_if

def on_connect(client):
    print("Conectado al broker MQTT")
    client.publish(CONNECTION_TOPIC, "Conexión exitosa")

def get_temperature():
    analog_value = adc.read()
    voltage = analog_value * 3.6 / 4095  # Convertir valor analógico a voltaje
    temperature = (voltage - 0.5) * 100  # Fórmula para calcular temperatura en grados Celsius
    return temperature

def publish_temperature(temperature):
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD, keepalive=0)
    client.set_callback(on_connect)
    client.connect()
    client.publish(MQTT_TOPIC, str(temperature))
    client.wait_msg()
    client.disconnect()

def display_temperature(temperature):
    oled.fill(0)
    oled.text("Temp: %.2f C" % temperature, 0, 0)
    oled.show()

sta_if = wifi_connect()

while True:
    temperature = get_temperature()
    display_temperature(temperature)
    publish_temperature(temperature)
    sleep(10)  # Esperar 10 segundos antes de leer la temperatura nuevamente
