import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from file import FsHandler
import time
import urequests

class WifiTools(object):
    def __init__(self, ssid, password, channel=3):
        self.ssid = ssid
        self.password = password
        self.wlan = None
        self.ifconfig = []
        self.channel = channel
        
    def ap_create(self):
        #Connect to WLAN
        self.wlan = network.WLAN(network.AP_IF)
        self.wlan.config(essid=self.ssid, password=self.password)
        self.wlan.active(True)
        while self.wlan.active() == False:
            pass
        
        return self.wlan.ifconfig()
    
    def client_create(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        print(self.channel)
        self.wlan.connect(self.ssid, self.password, channel=self.channel)
        #self.wlan.connect('Mamanet', 'HuboBubo22', channel=3)

      
        max_wait = 100
        while max_wait > 0:
            st = self.wlan.status()
            if st < 0 or st >= 3:
                break
            max_wait -= 1
            print(f"waiting for connection... {st}")
            time.sleep(1)

        # Handle connection error
        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print( 'ip = ' + status[0] )

        return self.wlan.ifconfig()



class HttpClient(object):
    def __init__(self, fs, remote_addr):
        self.fs = fs
        self.remote_addr = remote_addr

    def read_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        return lines

    def upload_all(self):
        allResult = True
        for filename in self.fs.glob(".*csv$"):
            if self.upload_file(filename) == False:
                allResult = False
        return allResult
            
    
    def upload_file(self, fname):
        payload = []
        payload.append({'filename': fname, 'content': self.read_file(fname)})
        #print(payload)
        try:
            print("Connecting to {} with payload {}".format(self.remote_addr, payload));
            response = urequests.post(self.remote_addr, json=payload)
            print(f"response={response}")
            if response.status_code != 200:
                #self.fs.alarm("can't upload {} to {}".format(fname, self.remote_addr))
                return False
            response.close()
            return self.fs.remove_file(fname)
        except Exception:
            return False
    