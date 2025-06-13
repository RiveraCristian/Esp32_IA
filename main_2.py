import network
import socket
from machine import Pin

led = Pin(4, Pin.OUT)

ssid = 'tu_SSID'
password = 'tu_contraseña'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

addr = socket.getaddrinfo('0.0.0.0', 80)[0]
s = socket.socket()
s.bind(addr)
s.listen(1)

print(' Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)

    if 'GET /led/on' in request:
        led.on()
        response = 'LED encendido'
    elif 'GET /led/off' in request:
        led.off()
        response = 'LED apagado'
    else:
        response = 'Petición no válida'

    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
    cl.send(response)
    cl.close()