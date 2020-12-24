#!/usr/bin/env python3
 
import sys
import os
import json
import paho.mqtt.client as mqtt
import subprocess
import shlex
 
MQTT_HOST = sys.argv[1]
MQTT_PORT = 1883
MQTT_USER = sys.argv[2]
MQTT_PASS = sys.argv[3]
MQTT_TOPIC = sys.argv[4]
# Messages posted to MQTT_TOPIC/MODEL_NAME/DEVICE_ID
PROTOCOL = sys.argv[5]
FREQUENCY = sys.argv[6]
GAIN = sys.argv[7]
OFFSET = sys.argv[8]
SAMPLE_RATE = sys.argv[9]

def on_connect(client, userdata, flags, rc):
    print("* MQTT connected")
 
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for line in popen.stdout:
        yield line
    popen.stdout.close()
 
client = mqtt.Client()
client.on_connect = on_connect
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()
 
 
if __name__ == '__main__':
    while True:
        last = ""
        for line in execute(shlex.split("rtl_433 -F json -R ", PROTOCOL, "-f ", FREQUENCY, "-g ", GAIN, "-p ", OFFSET, "-s ", SAMPLE_RATE, "-M newmodel -M level -M stats -C si")):
            if last != line:
                try:
                    data = json.loads(line)
                    model = data["model"]
                    devid = data["id"]
                    topic = "{}/{}/{}".format(MQTT_TOPIC,model,devid)
                    print(topic+" "+line)
                    log = open("/var/log/rtl433mqtt.log","a")
                    log.write(topic+" "+line)
                    log.close()
                    client.publish(topic,line)
                except json.decoder.JSONDecodeError:
                    pass
            last = line