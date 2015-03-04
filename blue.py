import bluetooth
import time
from threading import Thread
from Queue import Queue

device_list = ''
sock=''

connect=False
def find_devices():
    global device_list
    global sock
    global connect
    print len(device_list)
    while len(device_list) == 0:
        print "inside "
        device_list=bluetooth.discover_devices(lookup_names= True)

    for address,name in device_list:
        print address,name
        if name == 'MindWave Mobile':
            print "mindwave bluetooth is found"
            sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            connect = False
            while (not (connect)):
                try:
                    sock.connect((address,1))
                    connect = True
                    return sock
                except bluetooth.btcommon.BluetoothError as error:
                    print "some error",error
                    time.sleep(5)


def fill_mindwave_data(data_queue):

    global sock
    global connect
    while True:
        #receive 100 packets of data
        if (connect):
            while True:

                sock_data= sock.recv(100)


                for i in sock_data:
                    data_queue.put(ord(i))




sock = find_devices()
data_queue = Queue(maxsize=0)

print "now starting the thread "
t=Thread(target=fill_mindwave_data,args=(data_queue,))
t.setDaemon(True)
t.start()

while True:
    if not(data_queue.empty()):
        packet = []
        if data_queue.get() == 170:
            if data_queue.get() == 170:
                packet = [170,170]+[data_queue.get() for i in range(6)]
        if len(packet) > 5:
            if packet[3] == 2:
                print "poor signal detected"






    else:
        time.sleep(2)

