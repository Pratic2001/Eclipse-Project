from machine import UART, Pin, ADC
import utime
import _thread

onboard = Pin(25, Pin.OUT)
light = Pin(2, Pin.OUT)
fan = Pin(3, Pin.OUT)
signal = Pin(4, Pin.OUT, Pin.PULL_DOWN)
LDR = ADC(28)
stat = 0
light_val = 0
fan_val = 0
lights_auto_stat = 0
fan_auto_stat = 0
def read_uart():
    uart0 = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
    global stat
    while True:
        try:
            onboard.toggle()
            rxData = bytes()
            while uart0.any() > 0:
                rxData += uart0.readline()
            rxData = rxData.decode('utf-8').rstrip()
            if rxData is not '':
                rxData = int(rxData)
                stat = rxData
            #print(stat)
            utime.sleep(0.1)
        except exception as e:
            continue
def perform_autoLights():
    var = 0
    var = LDR.read_u16()
    if var <= 35000:
        #print("yay")
        light.value(1)
    elif var >= 46000:
        #print("Nop")
        light.value(0)
    #print(var)
    #utime.sleep(0.1)
    
_thread.start_new_thread(read_uart, ())
while True:
    if stat == 200:
        lights_auto_stat = 0
        fan_auto_stat = 0
        light_val = 0
        fan_val = 0
    if stat == 724 or stat == 24:
        lights_auto_stat = 0
        fan_auto_stat = 0
        light_val = 1
        fan_val = 0
    elif stat == 734 or stat == 834 or stat == 34:
        lights_auto_stat = 0
        fan_auto_stat = 0
        light_val = 0
        fan_val = 0
    elif stat == 825 or stat == 725:
        lights_auto_stat = 0
        fan_auto_stat = 0
        light_val = 1
        fan_val = 1
    elif stat == 735 or stat == 835:
        lights_auto_stat = 0
        fan_auto_stat = 0
        light_val = 0
        fan_val = 1
    elif stat == 824 or stat == 24:
        lights_auto_stat = 0
        fan_auto_stat = 0
        light_val = 1
        fan_val = 0
    elif stat == 814 or stat == 84:
        fan_auto_stat = 0
        lights_auto_stat = 1
        fan_val = 0
    elif stat == 85 or stat == 815:
        fan_auto_stat = 0
        lights_auto_stat = 1
        fan_val = 1
    elif stat == 763 or stat == 73:
        fan_auto_stat = 1
        lights_auto_stat = 0
        light_val = 0
        fan_val = 0
    elif stat == 72 or stat == 762:
        fan_auto_stat = 1
        lights_auto_stat = 0
        light_val = 1
        fan_val = 0
    elif stat == 1000:
        light_val = 0
        fan_val = 0
        lights_auto_stat = 1
        fan_auto_stat = 1
    elif stat == 7:
        lights_auto_stat = 0
    elif stat == 83:
        lights_auto_stat = 0
        fan_auto_stat = 0
        light_val = 0
    elif stat == 4:
        fan_val = 0
    elif stat == 5:
        fan_val = 1
    elif stat == 8:
        fan_auto_stat = 0
    if lights_auto_stat == 1:
        perform_autoLights()
    if fan_auto_stat == 1:
        signal.value(1)
    elif fan_auto_stat == 0:
        signal.value(0)
     
    if lights_auto_stat == 0:
        light.value(light_val)
    if fan_auto_stat == 0:
        fan.value(fan_val)
        
    







