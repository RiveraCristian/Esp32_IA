Claro, aquí tienes un ejemplo de un script en MicroPython que puedes usar para encender un LED conectado al pin 2 al recibir una señal HTTP. Este script se debe ejecutar en una placa compatible con MicroPython, como un ESP8266 o ESP32.

Primero, asegúrate de que tienes `network` y `socket` ya importados, y que estás conectado a tu red Wi-Fi. Aquí está el código:

```python
import network
import socket
from machine import Pin

# Configuración del LED
led = Pin(2, Pin.OUT)  # Pin 2 como salida

# Conectar a Wi-Fi
ssid = 'tu_ssid'
password = 'tu_contraseña'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print("Conectando a la red...")
    print("Conexión exitosa, IP:", wlan.ifconfig()[0])

# Conectar a Wi-Fi
connect_wifi()

# Crear un socket para el servidor HTTP
addr = socket.getaddrinfo('0.0.0.0', 80)  # Escuchar en todas las interfaces en el puerto 80
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Servidor HTTP en ejecución...")

while True:
    cl, addr = s.accept()
    print('Cliente conectado desde:', addr)
    request = cl.recv(1024)
    request = str(request)

    # Verificar la solicitud
    if 'GET /encender' in request:
        led.value(1)  # Encender el LED
        response = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
        response += '<h1>LED Encendido</h1>'
    elif 'GET /apagar' in request:
        led.value(0)  # Apagar el LED
        response = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
        response += '<h1>LED Apagado</h1>'
    else:
        response = 'HTTP/1.0 404 NOT FOUND\r\nContent-type: text/html\r\n\r\n'
        response += '<h1>Página no encontrada</h1>'

    cl.send(response)
    cl.close()
```

### Explicación del código:

1. **Configuración del LED**: El LED está conectado al pin 2 de la placa. Se configura como una salida.
   
2. **Conexión a Wi-Fi**: Se define una función `connect_wifi` que se encarga de conectar la placa a la red Wi-Fi utilizando el SSID y la contraseña proporcionados.

3. **Servidor HTTP**: Se crea un socket TCP que escucha en el puerto 80. Cuando un cliente se conecta, se obtiene la solicitud.

4. **Manejo de la solicitud**: Si la solicitud incluye `GET /encender`, el LED se enciende. Si incluye `GET /apagar`, el LED se apaga. Si no se encuentra la ruta, se devuelve un error 404.

### Cómo probarlo:
- Almacena este código en tu placa y ejecuta el script.
- Accede a la dirección IP de tu ESP en un navegador web o un cliente HTTP.
- Para encender el LED, navega a `http://tu_ip/encender`.
- Para apagar el LED, navega a `http://tu_ip/apagar`. 

Asegúrate de reemplazar `tu_ssid` y `tu_contraseña` por las credenciales correctas de tu red Wi-Fi.