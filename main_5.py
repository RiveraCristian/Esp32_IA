import network
import socket
from machine import Pin

led = Pin(4, Pin.OUT)

ssid = 'tu_ssid'
password = 'tu_contraseña'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(1)

while True:
    cl, addr = s.accept()
    request = cl.recv(1024)
    request = str(request)
    
    if 'GET /on' in request:
        led.value(1)
    if 'GET /off' in request:
        led.value(0)

    response = 'HTTP/1.1 200 OK\n\n'
    cl.send(response)
    cl.close()