import csv
import pandas as pd
import logging
import configparser
from time import time
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def main():
    config = readConfig()
    csv_has_header = config['Config'].getboolean('csv_has_header')
    rows_per_message = config['Config'].getint('rows_per_message')
    print(f'rows per message: {rows_per_message}')
    time_offset = config['Config'].getint('time_offset')
    time_step = config['Config'].getint('time_step')
    url = config['Config']['public_url_no_port']
    filename = config['Config']['csv_file']
    token = config['Config']['device_token']

    try: 
        client = connectMQTTclient(url, token, config)
        currentTimeMs = round(time() * 1000)
        startTime = currentTimeMs - time_offset #get current time in ms minus an offset
        messages = []

        with open(filename, 'r') as file:
            reader = csv.reader(file)
            idx = 0
            for row in reader:
                idx = idx + 1
                rowlist = list(map(float,row)) #Get the csv row as a list of floats
                messageTime = (startTime + (idx * time_step))
                messageData = {
                    "ts": messageTime,
                    "values": {"data": rowlist}
                }
                messages.append(messageData)
                if idx % rows_per_message == 0:
                    sendMQTT(client, messages)
                    messages = []
            if idx % rows_per_message != 0:
                sendMQTT(client, messages)
        exit()
    except Exception as e:
        print(f"Exception: {e}")
        if client:
            client.disconnect()

#parse config and return config object
def readConfig():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config

def getDataFrameFromCsv(filename):
    df = pd.read_csv(filename, header=None, memory_map=True, sep=',')
    return df

def startMQTTclients(url, tokens:pd.DataFrame, config):
    clients = []
    for token in tokens:
        client = connectMQTTclient(url, token, config)
        clients.append(client)
    return clients

def connectMQTTclient(url, token, config:configparser):
    max_inflight_val = config['Config'].getint('mqtt_max_inflight')
    rate_limit = config['Config']['mqtt_rate_limit']
    client = TBDeviceMqttClient(url, username=token, rate_limit=rate_limit)
    client.max_inflight_messages_set(max_inflight_val)
    client.connect()
    return client

def endMQTTclients(clients):
    for client in clients:
        client.disconnect()

def testMQTT():
    telemetry = {"temperature": 41.9}
    client = TBDeviceMqttClient("demo.thingsboard.io", username="t3D3PodiW2obWAYypFZQ")
    # Connect to ThingsBoard
    client.connect()
    # Sending telemetry without checking the delivery status
    client.send_telemetry(telemetry) 
    # Sending telemetry and checking the delivery status (QoS = 1 by default)
    result = client.send_telemetry(telemetry)
    # get is a blocking call that awaits delivery status  
    success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
    # Disconnect from ThingsBoard
    client.disconnect()

def sendMQTT(client, data:dict):
    result = client.send_telemetry(data)
    success = result.get() == TBPublishInfo.TB_ERR_SUCCESS
    return success


if __name__ == '__main__':
    main()

#mosquitto_pub -d -q 1 -h tb-route-node-root-thingsboard.apps.ociopenshift.test-app.cloud -p 1883 -t v1/devices/me/telemetry -u "63okHXnboSMhRw596aPF" -m "{temperature:25}"
#mosquitto_pub -d -q 1 -h demo.thingsboard.io -p 1883 -t v1/devices/me/telemetry -u "t3D3PodiW2obWAYypFZQ" -m "{temperature:25}"
#-d : debug
#-q : qos (Quality of service = 1)
#-h : host <url>
#-p : port <port>
#-t : topic <topic>
#-u : username <username> (token)
#-m : message <message> 
