from gps import GpsHandler
from client import HttpClient, WifiTools
from file import FsHandler
import machine
import time
import _thread
    

UARTx = 0
# define the rp2040 uart baudrate , the default baudrate is 9600 of L76B
BAUDRATE = 9600

def gps_handler(fs):
    gps = GpsHandler(UARTx, BAUDRATE, fs)
    #gps.fs.clear_all()
    gps.log_gps()

def client_handler(fs):
    client = HttpClient(fs, 'http://192.168.1.106:8000/gps')
    return client.upload_all()
    
fs = FsHandler()
t = _thread.start_new_thread(gps_handler, [fs])

wifiTools = WifiTools('Mamanet', 'HuboBubo22')
cfg = wifiTools.client_create()
ip = cfg[0]
print(f"Client ip obtained from AP: {ip}")
while True:
    upload = client_handler(fs)
    print(f"Upload: {upload}")
    time.sleep(1)
