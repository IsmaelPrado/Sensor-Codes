from machine import Pin, PWM
import time

# Configuración de pines para el KY-005 IR Emitter y el KY-022 IR Receiver
pin_emisor = Pin(13, Pin.OUT)  # Pin para el emisor infrarrojo
pin_receptor = Pin(12, Pin.IN)  # Pin para el receptor infrarrojo

# Función para encender el emisor infrarrojo
def encender_emisor():
    pin_emisor.on()

# Función para apagar el emisor infrarrojo
def apagar_emisor():
    pin_emisor.off()

# Función para detectar la presencia de la señal infrarroja
def detectar_infrarrojo():
    return pin_receptor.value()

# Encender el emisor infrarrojo
encender_emisor()

# Bucle principal para detectar la señal infrarroja
while True:
    if detectar_infrarrojo():
        print("Se ha detectado la señal infrarroja.")
    else:
        print("No se ha detectado la señal infrarroja.")
    time.sleep(0.1)  # Espera 100 milisegundos entre las detecciones
