import network
import socket
import time
from machine import Pin, PWM

SSID = 'KenMau'
netpass = '12.Kweku.12'
powerlevel = 255
powerpin = 25
dironepin = 15
dirtwopin = 16

motorpower = PWM(Pin(powerpin))
motorpower.freq(50)
onedir = Pin(dironepin, mode=Pin.OUT)
twodir = Pin(dirtwopin, mode=Pin.OUT)
flipswitch = 0

def webconn(server, port, url, argument):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(socket.getaddrinfo(server, port)[0][-1])
    s.write('GET '+url+'?'+argument+' HTTP/1.1\nHost: '+server+'\nConnection: close\n\n')
    replypart = 'a'
    reply = ''
    while replypart:
        replypart = s.recv(4096)
        reply = reply + replypart.decode('utf-8')
    s.close()
    replylist = reply.split('\n')
    return replylist[len(replylist)-1]       

sta_if = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)
ap.active(False)
gotthrough = False

if not sta_if.isconnected():
    sta_if.active(True)
    while not gotthrough:
        try:
            print('Connecting to network...')
            sta_if.connect(SSID, netpass)
            while not sta_if.isconnected():
                pass
            gotthrough = True
        except:
            gotthrough = False

myip = sta_if.ifconfig()[0]
print(myip)
a = sta_if.config('mac')
macaddrtxt = '{:02x}-{:02x}-{:02x}-{:02x}-{:02x}-{:02x}'
macaddr = macaddrtxt.format(a[0], a[1], a[2], a[3], a[4], a[5])
print(macaddr)

webconn('cecq8z.com', 80, '/arduino/arduinoregister.php', 'boardid=bc-3e-07-fa-b4-28') 

while True:
    x = 0
    if flipswitch == 0:
        webconn('cecq8z.com', 80, '/arduino/arduinomotor.php', 'boardid=bc-3e-07-fa-b4-28')
        print('Motor should be spinning in one direction then slowing down')
        onedir.on()
        twodir.off()
    else:
        webconn('cecq8z.com', 80, '/arduino/arduinomotor.php', 'boardid=bc-3e-07-fa-b4-28')
        print('Motor should be spinning in the other direction then slowing down')
        onedir.off()
        twodir.on()
    motorpower.duty_u16(65535)
    for x in range(255):
        motorpower.duty_u16(65535 - (x * 256))
        time.sleep_ms(100)
    if flipswitch == 0:
        flipswitch = 1
    else:
        flipswitch = 0
