from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import json
import boto3
import pyaudio

polly = boto3.client("polly", region_name=region)
pya = pyaudio.PyAudio()

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

def speak(text, voice="Joanna")
    try:
        # Request speech synthesis
        response = polly.synthesize_speech(Text=text_string,
            TextType="text", OutputFormat="pcm", VoiceId=voice)
    except (BotoCoreError, ClientError) as error:
        # The service returned an error, exit gracefully
        print(error)
        exit(-1)
    # Access the audio stream from the response
    if "AudioStream" in response:
        stream = pya.open(format=pya.get_format_from_width(width=2), channels=1, rate=16000, output=True)
        stream.write(response['AudioStream'].read())
        sleep(1)
        stream.stop_stream()
        stream.close()
    else:
        # The response didn't contain audio data, return False
        print("Could not stream audio")
        return(False)

host = 'a2lmtd0lp0ntdm-ats.iot.eu-west-1.amazonaws.com'
rootCAPath = '/home/pi/IoT/MQTT/certs/root_ca.pem'
certificatePath = '/home/pi/IoT/MQTT/certs/0731350cf7-certificate.pem.crt'
privateKeyPath = '/home/pi/IoT/MQTT/certs/0731350cf7-private.pem.key'
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
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Loop forever
loopCount = 0
while True:
    time.sleep(1)
