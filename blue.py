import bluetooth
import time
device_list = ''
while len(device_list) == 0:
    device_list=bluetooth.discover_devices(lookup_names= True)

for address,name in device_list:
    print address,name
    if name == 'MindWave Mobile' or len(name) > 0:
        print "mindwave bluetooth is found"
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        connect = False
        while (not (connect)):
            try:
                socket.connect((address,2))
                connect = True
            except bluetooth.btcommon.BluetoothError as error:
                print "some error",error
                time.sleep(5)

        if (connect):
            while True:
                sock_data= socket.recv(100)
                data=map(ord,sock_data)
                print data

            print "device connected"
            socket.close()












