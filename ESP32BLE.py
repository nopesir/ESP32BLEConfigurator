import gatt


class ESP32BLEManager(gatt.DeviceManager):
    hashmac = {}
    i = 0

    def device_discovered(self, device):
        if "esp32" in device.alias():
            self.i+=1
            self.hashmac[device.mac_address] = device.alias()
            if self.i >= 5:
                self.stop()
            


class ESP32BLE(gatt.Device):

    i = 0
    serv = ''
    char_1 = ''
    char_2 = ''
    char_3 = ''
    password = ''
    ssid = ''
    ip_address = ''
    name = ''


    def __init__(self, ssid, password, mac_address, manager, name, ip_address):
        super().__init__(mac_address, manager, ip_address)
        self.password = password
        self.ssid = ssid
        self.ip_address = ip_address
        self.name = name

    def connect_succeeded(self):
        super().connect_succeeded()
        print("Connected to %s" % (self.name))

    def connect_failed(self, error):
        super().connect_failed(error)
        print("[%s] Connection failed: %s" % (self.mac_address, str(error)))
        self.manager.stop()

    def disconnect_succeeded(self):
        super().disconnect_succeeded()
        print("[%s] Disconnected" % (self.mac_address))


    def services_resolved(self):
        super().services_resolved()
        
        self.serv = next(
        s for s in self.services
        if s.uuid == '5f6d4f53-5f43-4647-5f53-56435f49445f')

        self.char_1 = next(
        c for c in self.serv.characteristics
        if c.uuid == '306d4f53-5f43-4647-5f6b-65795f5f5f30')

        self.char_2 = next(
        c for c in self.serv.characteristics
        if c.uuid == '316d4f53-5f43-4647-5f76-616c75655f31')

        self.char_3 = next(
        c for c in self.serv.characteristics
        if c.uuid == '326d4f53-5f43-4647-5f73-6176655f5f32')
        print("------------------------------")
        self.char_1.write_value(b'wifi.sta.ssid')
        #b = bytes('Mammellata', 'ascii')  
        
        
    
    def characteristic_write_value_succeeded(self, characteristic):
        super().characteristic_write_value_succeeded(characteristic)
        self.i+=1

        if self.i == 1:
            a = bytes(self.ssid, 'utf-8')
            self.char_2.write_value(a)
        
        if self.i == 2:
            self.char_3.write_value(b'1')

        if self.i == 3:
            print("Write OK for wifi.sta.ssid")
            self.char_1.write_value(b'wifi.sta.pass')
        
        if self.i == 4:
            self.char_2.write_value(bytes(self.password, 'utf-8'))

        if self.i == 5:
            self.char_3.write_value(b'1')

        if self.i == 6:
            print("Write OK for wifi.sta.pass")
            self.char_1.write_value(b'bt.keep_enabled')

        if self.i == 7:
            self.char_2.write_value(b'true')

        if self.i == 8:
            self.char_3.write_value(b'1')

        if self.i == 9:
            print("Write OK for bt.keep_enabled")
            self.char_1.write_value(b'mqtt.server')

        if self.i == 10:
            host_ip = bytes(self.ip_address, 'utf-8')
            self.char_2.write_value(host_ip)

        if self.i == 11:
            self.char_3.write_value(b'1')

        if self.i == 12:
            print("Write OK for mqtt.server")
            self.char_1.write_value(b'mqtt.enable')

        if self.i == 13:
            self.char_2.write_value(b'true')

        if self.i == 14:
            self.char_3.write_value(b'1')

        if self.i == 15:
            print("Write OK for mqtt.enable")
            self.char_1.write_value(b'wifi.ap.enable')

        if self.i == 16:
            self.char_2.write_value(b'false')

        if self.i == 17:
            self.char_3.write_value(b'1')

        if self.i == 18:
            self.char_1.write_value(b'wifi.sta.enable')

        if self.i == 19:
            self.char_2.write_value(b'true')

        if self.i == 20:
            print("Write OK for wifi.sta.enable")
            self.char_3.write_value(b'2')
        
        if self.i >= 21:
            self.manager.stop()
        
    def characteristic_value_updated(self, characteristic, value):
        super().characteristic_value_updated(characteristic, value)
        print("Updated!")


    def characteristic_write_value_failed(self, error, characteristic):
        super().characteristic_write_value_failed(error, characteristic)
        print("error, ", error)
        self.manager.stop()
