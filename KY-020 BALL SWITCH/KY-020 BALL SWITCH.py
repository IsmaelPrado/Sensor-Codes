from machine import Pin
import time

# Configuración de los pines
ball_switch_pin = Pin(16, Pin.IN)  # Pin del sensor KY-020 Ball Switch conectado al pin 16

# Bucle principal
while True:
    if ball_switch_pin.value() == 1:  # Si el sensor detecta (valor 1)
        print("Sensor detectado")
    else:
        print("Sensor no detectado")

    time.sleep(1)  # Esperar 1 segundo antes de la próxima medición
