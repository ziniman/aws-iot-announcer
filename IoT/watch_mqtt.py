#! /usr/bin/env python

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
import boto3
from botocore.exceptions import BotoCoreError, ClientError
import os
import random
import pygame

region = 'eu-west-1'
polly = boto3.client("polly", region_name=region)
script_path = os.path.dirname(__file__)

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    data = json.loads(message.payload)
    tts = data["tts"]
    voices = ["Joey", "Matthew", "Joanna", "Kendra", "Salli", "Brian", "Amy"]
    voice = voices[random.randrange(len(voices))]
    print("Calling TTS with %s [%s]" % (tts, voice))
    speak (tts, voice)


def speak(text_string, voice="Joanna"):
    try:
        # Request speech synthesis
        text_string = '<speak><amazon:effect name="drc">%s</amazon:effect></speak>' % text_string
        response = polly.synthesize_speech(Text=text_string,
            TextType="ssml", OutputFormat="mp3", VoiceId=voice)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        exit(-1)
    # Access the audio stream from the response
    print (response)
    if "AudioStream" in response:
        file = open('%s/speech.mp3' % script_path, 'w')
        file.write(response['AudioStream'].read())
        file.close()
        pygame.mixer.init(48000, -16, 1, 1024)
        pygame.mixer.music.load('%s/ding.mp3' % script_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        pygame.mixer.music.load('%s/speech.mp3' % script_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(1)

        pygame.mixer.quit()#os.system('mpg123 -m ding.mp3 speech.mp3 &')
    else:
        # The response didn't contain audio data, return False
        print("Could not stream audio")
        return(False)

host = 'a2lmtd0lp0ntdm-ats.iot.eu-west-1.amazonaws.com'
rootCAPath = '/home/pi/IoT/MQTT/certs/root_ca.pem'
certificatePath = '/home/pi/IoT/MQTT/certs/2b0eccd4d9-certificate.pem.crt'
privateKeyPath = '/home/pi/IoT/MQTT/certs/2b0eccd4d9-private.pem.key'
port = 8883
useWebsocket = False
clientId = 'Floor28Announcer'
topic = '$aws/things/Floor28_RBPi/announce'


# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, port)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 0, customCallback)
time.sleep(2)

# Loop forever
loopCount = 0
while True:
    time.sleep(1)
