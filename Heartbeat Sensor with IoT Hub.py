# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in https://github.com/Azure-Samples/azure-iot-samples-python/archive/master.zip
# geektechstuff

import random
import time
import sys

# imports the modules for the sensor
import RPi.GPIO as GPIO
import time


def handle_heartrate(chl):

    global channel
    global count
    global doCounting
    global startTime
    global currentTime
    global heartbeat1

    channel = chl
    count = count + 1
    
    # print('Count is {}'.format(count))
    
    if not doCounting:

        if count == 5:
            
            print('Starting actual counting...')
            
            startTime = time.time()
            count = 0
            doCounting = True                
        
    if doCounting:
        
        currentTime = time.time()
                
        if currentTime - startTime > 10:
            
            if count > 0:
                heartbeat1=count*4
                
                print('Heart rate is {}'.format(str(count * 4)))
            
            startTime = time.time()
            count = 0
    return heartbeat1
                                   
# pin definition
channel = 0
heartPin = 16
ledPin = 40
butPin = 38
count = 0
doCounting = False
startTime = 0.0
currentTime = 0.0
doMeasureHeartRate = False

# pin setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(heartPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('Program running... Press Ctrl+C to exit')

try:
    
    GPIO.output(ledPin, False)        
    
    while(True):
        
        if not GPIO.input(butPin):
            
            if not doMeasureHeartRate:
                
                print('Measuring heart rate...')
                
                doMeasureHeartRate = True;
                GPIO.output(ledPin, True)
                
                count = 0
                doCounting = False
                startTime = time.time()
                currentTime = 0.0
                
                GPIO.add_event_detect(heartPin, GPIO.RISING, callback = handle_heartrate)
                
            else:
                
                print('Stopped...')
                
                doMeasureHeartRate = False;
                GPIO.output(ledPin, False)                            
                GPIO.remove_event_detect(channel)
                
            time.sleep(0.2)
            
        if doMeasureHeartRate:
            
            currentTime = time.time()
            
            if currentTime - startTime > 15:
                
                print('Still waiting for heart beat...')
                                            
                startTime = time.time()
                count = 0
                doCounting = False
    
except KeyboardInterrupt:
    pass
    
except Error as err:
    
    print('An error has occurred: {}'.format(err))

finally:
    
    GPIO.cleanup()    




# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
# The sample connects to a device-specific MQTT endpoint on your IoT Hub.
import iothub_client
# pylint: disable=E0611
from iothub_client import IoTHubClient, IoTHubClientError, IoTHubTransportProvider, IoTHubClientResult
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult, IoTHubError, DeviceMethodReturnValue

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=G6NUS2019.azure-devices.net;DeviceId=ruchika;SharedAccessKey=/8oRKSgCxpw/wz/shB+Gx7GhMnVZ61RGxDaApWFnn20="

# Using the MQTT protocol.
PROTOCOL = IoTHubTransportProvider.MQTT
MESSAGE_TIMEOUT = 10000
# Define the JSON message to send to IoT Hub.
HEARTBEAT = handle_heartrate(channel)
MSG_TXT = "{\"Heartbeat\": %.2f}"

def send_confirmation_callback(message, result, user_context):
    print ( "IoT Hub responded to message with status: %s" % (result) )

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )

        while True:
            # Build the message with simulated telemetry values.
            heart_beat=HEARTBEAT
            msg_txt_formatted = MSG_TXT % (heart_beat)
            message = IoTHubMessage(msg_txt_formatted)

            

            # Send the message.
            print( "GeekTechStuff Azure Sending Message: %s" % message.get_string() )
            client.send_event_async(message, send_confirmation_callback, None)
            time.sleep(30)

    except IoTHubError as iothub_error:
        print ( "Unexpected error %s from IoTHub" % iothub_error )
        return
    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    iothub_client_telemetry_sample_run()
