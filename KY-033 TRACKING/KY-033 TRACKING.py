from machine import Pin
import time

sensor_pin = Pin(13, Pin.IN)  # Pin del sensor KY-033
led_pin = Pin(4, Pin.OUT)     # Pin del LED

while True:
    valor_sensor = sensor_pin.value()  # Leer el estado del sensor

    # Si el sensor detecta algo blanco (estado 0), encender el LED; de lo contrario, apagarlo
    if valor_sensor == 0:
        led_pin.on()  # Encender el LED
    else:
        led_pin.off()  # Apagar el LED

    time.sleep_ms(100)  # Pequeña pausa para estabilidad
