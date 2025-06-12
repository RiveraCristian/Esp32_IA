import network
import socket
from machine import Pin

led = Pin(2, Pin.OUT)

ssid = 'tu_SSID'
password = 'tu_CONTRASEÑA'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(1)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    
    if 'GET /led/on' in request:
        led.value(1)
    elif 'GET /led/off' in request:
        led.value(0)
    
    response = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\nLED control'
    conn.sendall(response.encode())
    conn.close()