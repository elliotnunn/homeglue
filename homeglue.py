import can
import paho.mqtt.client as mqtt
import threading

def send_can_msg(msg_bytes):
    can_bus.send(can.Message(arbitration_id=0, extended_id=False, data=bytearray(msg_bytes)))

# Allocate serialisation lock
big_lock = threading.Lock()

# Set up can_bus and callback
bustype = 'socketcan_native'
channel = 'can0'

def can_callback(msg):
    with big_lock:
        first_byte = msg.data[0]

can_bus = can.interface.Bus(channel=channel, bustype=bustype)

# Set up mqtt and callback
def mqtt_callback(client, userdata, msg):
    with big_lock:
        # topic, payload, qos, retain
        if msg.topic == 'blinds/elliot_north':
            if msg.payload = 'UP':
                send_can_msg([0x4D, 0x01, 0xFF]); send_can_msg([0x4D, 0x02, 0xFF])
            elif msg.payload == 'DOWN':
                send_can_msg([0x4D, 0x01, 0x77]); send_can_msg([0x4D, 0x02, 0x77])
        elif msg.topic == 'blinds/elliot_west':
            if msg.payload = 'UP':
                send_can_msg([0x4D, 0x00, 0xFF])
            elif msg.payload == 'DOWN':
                send_can_msg([0x4D, 0x00, 0x77])

mqtt_client = mqtt.Client()
mqtt_client.on_connect = lambda: mqtt_client.subscribe('#')
mqtt_client.on_message = mqtt_callback

# Start both loops
notifier = can.Notifier(can_bus, [can_callback])
while 1: mqtt_client.loop()

#msg = can.Message(arbitration_id=0xc0ffee, data=[id, i, 0, 1, 3, 1, 4, 1], extended_id=False)
#can_bus.send(msg)
