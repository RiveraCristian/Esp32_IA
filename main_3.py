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

print('Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    
    if '/on' in request:
        led.value(1)
    elif '/off' in request:
        led.value(0)

    response = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
    response += '<html><body><h1>LED Control</h1>'
    response += '<p><a href="/on">Turn LED On</a></p>'
    response += '<p><a href="/off">Turn LED Off</a></p>'
    response += '</body></html>'
    
    cl.send(response)
    cl.close()