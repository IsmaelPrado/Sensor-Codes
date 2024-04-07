from machine import Pin, PWM
import time

# Configuración de pines para el LED RGB
led_red = PWM(Pin(13), freq=1000)   # Pin para el color rojo
led_green = PWM(Pin(14), freq=1000) # Pin para el color verde
led_blue = PWM(Pin(12), freq=1000)  # Pin para el color azul

# Función para cambiar el color del LED RGB
def set_color(red, green, blue):
    led_red.duty(red)     # Configurar el brillo del color rojo
    led_green.duty(green) # Configurar el brillo del color verde
    led_blue.duty(blue)   # Configurar el brillo del color azul

# Ciclo para cambiar gradualmente el color del LED RGB
while True:
    # Cambio gradual a amarillo
    for i in range(1024):
        set_color(i, i, 0)
        time.sleep_ms(1)
    # Cambio gradual a verde cian
    for i in range(1024):
        set_color(0, i, i)
        time.sleep_ms(1)
    # Cambio gradual a azul
    for i in range(1024):
        set_color(0, 1023 - i, 1023)
        time.sleep_ms(1)
    # Cambio gradual a magenta
    for i in range(1024):
        set_color(i, 0, 1023 - i)
        time.sleep_ms(1)
    # Cambio gradual a rojo
    for i in range(1024):
        set_color(1023, i, 0)
        time.sleep_ms(1)
