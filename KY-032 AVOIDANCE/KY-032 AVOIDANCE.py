from machine import Pin
import time

# Configuración de pines
sensor_out_pin = Pin(13, Pin.IN)  # Pin OUT del sensor KY-032
led_pin = Pin(4, Pin.OUT)          # Pin del LED

while True:
    valor_sensor = sensor_out_pin.value()  # Leer el estado del sensor

    # Si el sensor detecta un objeto cercano (estado 1), encender el LED; de lo contrario, apagarlo
    if valor_sensor == 0:
        led_pin.on()  # Encender el LED
    else:
        led_pin.off()  # Apagar el LED

    time.sleep_ms(100)  # Pequeña pausa para estabilidad
