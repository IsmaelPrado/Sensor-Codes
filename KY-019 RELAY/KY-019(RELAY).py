from machine import Pin, PWM, I2C
import ssd1306 
import time
from umqtt.simple import MQTTClient
import network
from time import sleep

MQTT_BROKER = "172.20.10.3"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "sensor/relay"
MQTT_PORT = 1883

# Definimos los pines para el relé, el buzzer, el botón y la pantalla OLED
RELAY_PIN = 13
BUZZER_PIN = 12
BUTTON_PIN = 14

# Inicializamos los pines
relay = Pin(RELAY_PIN, Pin.OUT)
buzzer_pwm = PWM(Pin(BUZZER_PIN, Pin.OUT))
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Inicializamos la comunicación I2C para la pantalla OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Pines SDA y SCL de la Raspberry Pi
oled = ssd1306.SSD1306_I2C(128, 32, i2c)

def wifi_connect():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print("Connect", end="")
    sta_if.connect("ElGerasxd", "xdpapi23")
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("Wifi connected")
    
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


# Función para encender el relé y hacer sonar el buzzer
def encender_rele_y_buzzer():
    relay.value(1)  # Encender el relé
    # Hacemos sonar el buzzer con una frecuencia de 1000 Hz
    buzzer_pwm.freq(1000)
    buzzer_pwm.duty(512)  # Duty cycle del 50% para una intensidad media
    print("Relé encendido")
    print("Buzzer sonando")

# Función para apagar el relé y el buzzer
def apagar_rele_y_buzzer():
    relay.value(0)  # Apagar el relé
    buzzer_pwm.duty(0)  # Apagar el buzzer
    print("Relé apagado")
    print("Buzzer apagado")

# Bucle principal
while True:
    button_value = button.value()  # Leer el valor del botón

    # Imprimir el valor del botón en la consola
    print("Valor del botón:", button_value)

    # Mostrar el valor del botón en la pantalla OLED
    oled.fill(0)  # Limpiar la pantalla
    oled.text("Boton:", 0, 0)
    oled.text(str(button_value), 60, 0)
    oled.show()

    if button_value == 0:  # Verificar si el botón está presionado (botón activado por pull-up)
        encender_rele_y_buzzer()
        client.publish(MQTT_TOPIC, button_value)
        while button.value() == 0:  # Esperar a que se suelte el botón
            time.sleep(0.1)
        apagar_rele_y_buzzer()
        client.publish(MQTT_TOPIC, button_value)
