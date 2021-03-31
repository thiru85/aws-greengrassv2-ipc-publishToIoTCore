# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0.
# Author: Thirumalai Aiyalu (taiyalu@amazon.com)
# Modified from AWS IoT SDK v2 for Python

import json
import time
import os
import random

import awsiot.greengrasscoreipc
import awsiot.greengrasscoreipc.model as model

if __name__ == '__main__':
    ipc_client = awsiot.greengrasscoreipc.connect()
    
    while True:
        telemetry_data = {
            "timestamp": int(round(time.time() * 1000)),
            "battery_state_of_charge": random.randint(40,50),
            "location": {
                "longitude": random.uniform(45,60),
                "latitude": random.uniform(45,70),
            },
        }

        op = ipc_client.new_publish_to_iot_core()
        op.activate(model.PublishToIoTCoreRequest(
            topic_name="my/iot/raspi4gg/telemetry",
            qos=model.QOS.AT_LEAST_ONCE,
            payload=json.dumps(telemetry_data).encode(),
        ))
        try:
            result = op.get_response().result(timeout=5.0)
            print("successfully published message:", result)
        except Exception as e:
            print("failed to publish message:", e)

        time.sleep(3)
