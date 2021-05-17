# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
# Author: Thirumalai Aiyalu (taiyalu@amazon.com)
# Modified from AWS IoT SDK v2 for Python

import json
import time
import os
import random
import socket

import paho.mqtt.client as mqtt #import the client1
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    
    ipc_client = awsiot.greengrasscoreipc.connect()

    hostname = socket.gethostname()
    
    ip_address = socket.gethostbyname(hostname)
       
    msg = subscribe.simple("localData/#", hostname=ip_address)
    localTopic=msg.topic
    messageBody=msg.payload
    print("Received %s on topic: %s" % (messageBody, localTopic))
    #This is assuming the topic being published is of the form n/n/n, like localdata/esp32-1/temperature etc
    topicSplitter=localTopic.split('/')

    cloudTopic="cloudData/"+topicSplitter[1]+"/"+topicSplitter[2]


    while True:
        
        msg = subscribe.simple("localData/#", hostname=ip_address)
        
        localTopic=msg.topic
        messageBody=msg.payload
        
        print('Received %s on topic: %s' % (messageBody, localTopic))

        # This is assuming the topic being published is of the form n/n/n, like localdata/esp32-1/temperature etc
        topicSplitter=localTopic.split('/')

        telemetry_data = {
            "timestamp": int(round(time.time() * 1000)),
            "battery_state_of_charge": random.randint(40,50),
            "location": {
                "longitude": random.uniform(45,60),
                "latitude": random.uniform(45,70),
            },
            "sensor_data":random.choice(topicSplitter),
        }

        op = ipc_client.new_publish_to_iot_core()
        op.activate(model.PublishToIoTCoreRequest(
            topic_name=cloudTopic,
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(telemetry_data).encode(),
        ))
        try:
            result = op.get_response().result(timeout=5.0)
            print("successfully published message:", result)
            print(telemetry_data)
            print()
        except Exception as e:
            print("failed to publish message:", e)

        time.sleep(3)
