# code to read and interpret mindwave data


import bluetooth
import time
from threading import Thread
from Queue import Queue
import matplotlib.pyplot as plt
from drawnow import *

device_list = ''
sock=''
wave1=[]
wave2=[]
plt.ion()

connect=False


plt.ylim(0,255)
plt.title('mindwave information')
plt.grid(True)
plt.ylabel('signal strenght')

plt.legend(loc='upper left')
plt2=plt.twinx()
plt.ylim(0,255)

plt2.set_ylabel('wave 2')
plt2.ticklabel_format(userOffset=False)
plt2.legend(loc='upper right')

def find_devices():
    global device_list
    global sock
    global connect
    print len(device_list)
    while len(device_list) == 0:
        print "inside "
        print device_list
        device_list=bluetooth.discover_devices(lookup_names= True)
    print device_list
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
counter=0
raw_data =[]
raw_data1=[]
while True:
    if not(data_queue.empty()):
        packet = []

        if data_queue.get() == 170:
            if data_queue.get() == 170:
                packet_length = data_queue.get()
                packet = [data_queue.get() for i in range(packet_length)]

                if packet[0] == 128:
                    wave1.append(packet[2])
                    wave2.append(packet[3])
                    #drawnow(graph)

                    plt.plot(wave1,'ro-',label='wave 1')
                    plt2.plot(wave2,'b^-',label='wave 2')
                    plt.pause(.001)
                    #print packet,wave1,wave2
                    counter += 1
                    if counter>30:
                        wave1.pop(0)
                        wave2.pop(0)




                if packet[0] == 2:

                    print "              "
                    print "              "
                    if packet[1]== 200:
                        print "SIGNAL QUALITY : POOR"
                    else:
                        print "SIGNAL QUALITY : GOOD"

                    print packet_length
                    print "MEDITATION :",packet[packet_length-1]
                    print "FOCUS :",packet[packet_length - 3]
        if len(raw_data) > 10000:
            break



    else:
        time.sleep(2)

