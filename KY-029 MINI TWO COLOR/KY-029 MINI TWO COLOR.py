from machine import Pin
import time

# Configuración de pines para el KY-011 Two Color
pin_rojo = Pin(12, Pin.OUT)  # Pin para el color rojo
pin_verde = Pin(14, Pin.OUT)  # Pin para el color verde

# Función para encender el color rojo y apagar el verde
def encender_rojo():
    pin_rojo.on()
    pin_verde.off()

# Función para encender el color verde y apagar el rojo
def encender_verde():
    pin_verde.on()
    pin_rojo.off()

# Encender el color rojo durante 3 segundos, luego el verde durante 3 segundos
while True:
    encender_rojo()  # Encender el color rojo
    time.sleep(3)    # Esperar 3 segundos
    encender_verde()  # Encender el color verde
    time.sleep(3)    # Esperar 3 segundos

