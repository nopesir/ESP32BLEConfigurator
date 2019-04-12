import gatt
import time
import socket
from ESP32BLE import ESP32BLE
from ESP32BLE import ESP32BLEManager
from tkinter import *

class takeInput(object):

    def __init__(self,requestMessage):
        self.root = Tk()
        self.string = ''
        self.frame = Frame(self.root)
        self.frame.pack()        
        self.acceptInput(requestMessage)

    def acceptInput(self,requestMessage):
        r = self.frame

        k = Label(r,text=requestMessage)
        k.pack(side='left')
        self.e = Entry(r,text='Name')
        self.e.pack(side='left')
        self.e.focus_set()
        b = Button(r,text='okay',command=self.gettext)
        b.pack(side='right')

    def gettext(self):
        self.string = self.e.get()
        self.root.destroy()

    def getString(self):
        return self.string

    def waitForInput(self):
        self.root.mainloop()

def getText(requestMessage):
    msgBox = takeInput(requestMessage)
    #loop until the user makes a decision and the window is destroyed
    msgBox.waitForInput()
    return msgBox.getString()

ssid = getText('Enter the SSID')
passwd = getText('Enter the password')
#ssid = str(input("Enter the SSID: "))
#passwd = str(input("Enter the password: "))

manager = ESP32BLEManager(adapter_name='hci0')
manager.start_discovery()
manager.run()
manager.stop_discovery()

macs = manager.hashmac

ip_address = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), 
s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, 
socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

for key,value in macs.items():
    manager = gatt.DeviceManager(adapter_name='hci0')
    device = ESP32BLE(ssid=ssid, password=passwd, manager=manager, mac_address=key,name=value, ip_address=ip_address)
    device.connect()

    manager.run()
    print("Rebooting %s" % value + '..')
    device.disconnect()
    print("------------------------------")



n_of_devices = len(macs)
names = macs.values()

# TO BE INTEGRATED WITH THE APP RUNNING WITH THE GUI ON RASPBERRY
