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

print('Conectado a la red:', wlan.ifconfig())

addr = socket.getaddrinfo('0.0.0.0', 80)[0]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Escuchando en', addr)

while True:
    cl, addr = s.accept()
    print('Cliente conectado desde', addr)
    request = cl.recv(1024)
    request = str(request)
    
    if 'GET /on' in request:
        led.value(1)
    elif 'GET /off' in request:
        led.value(0)

    cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    cl.send('<h1>LED control</h1><p>Use /on to turn on the LED and /off to turn it off.</p>')
    cl.close()