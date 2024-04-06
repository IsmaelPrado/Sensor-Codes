from machine import Pin, PWM
import time

# Configuración de los pines
button_pin = Pin(23, Pin.IN)  # Pin del botón KY-004 conectado al pin 23
servo_pin = Pin(15, Pin.OUT)  # Pin de control del servo conectado al pin 18
servo_pwm = PWM(servo_pin, freq=50)  # Configurar PWM para el servo a 50Hz
led_pin = Pin(2, Pin.OUT)

# Función para mover el servo a una posición específica
def move_servo(angle):
    duty = int((angle / 180) * 1024 + 102)  # Cálculo del ciclo de trabajo como entero
    servo_pwm.duty(duty)
    time.sleep(0.5)  # Esperar un momento después de mover el servo

# Bucle principal
while True:
    button_value = button_pin.value()  # Leer el valor del botón
    print("Valor del botón:", button_value)  # Imprimir el valor del botón
    if button_value == 1:  # Si el botón está presionado (valor 0)
        move_servo(90)  # Mover el servo a 90 grados
        led_pin.value(1)
        print("Servo activado")
    else:
        move_servo(0)
        led_pin.value(0)# Si no, mantener el servo en posición inicial (0 grados)
       
