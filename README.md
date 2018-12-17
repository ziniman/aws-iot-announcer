# aws-iot-announcer
A simple app that is using a RaspberryPi device controlled by an AWS IoT Button to play public announcement using Amazon Polly as the TTS engine.

## IoT
This folder includes the code running on the RaspberryPi device.

### IoT Requirements
This part of the app is running on a RaspberryPi (Tested on Model B+ and above) and require the following components to run the code:

#### pip (only on RaspberryPi light installation)
You will need pip to install some python packages.
```
sudo apt-get update
sudo apt-get install python-pip
```

#### AWS CLI
The AWS CLI is an open source tool that provides commands for interacting with AWS services. With minimal configuration, you can start using all of the functionality provided by the AWS Management Console from your favorite terminal program.
AWS CLI will allow you to define your user credentials to access your AWS account and invoke different services. In our case, we need access   to AWS Polly (Text to speech Service) to convert the announcements into sound files.

```
pip install awscli --upgrade --user
export PATH=~/.local/bin:$PATH
```

After installation, please run ```aws configure``` to configure your account. Full details on how to configure you account can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

#### boto3
[Boto](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) is the Amazon Web Services (AWS) SDK for Python, which allows Python developers to write software that makes use of Amazon services like S3, EC2 and IoT. You will need to install boto3 using the next command.

```
pip install boto3
```
After installation, please follow these [instruction](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) to configure your environment.

#### AWSIoTMQTTClient
The AWS IoT Device SDK for Python allows developers to write Python script to use their devices to access the AWS IoT platform through MQTT or MQTT over the WebSocket protocol.
```
pip install AWSIoTPythonSDK
```
For setup and configuration details check the [github repository](https://github.com/aws/aws-iot-device-sdk-python).

#### pygame setup (RaspberryPi lite version only)
Make sure you install pygame to be able to play sounds from your python code.
```
sudo apt-get install python-pygame
```

### IoT Security & Certificates
To enable a secure connection between your RaspberryPi and AWS IoT, you have to download and install AWS IoT core certificates on your device.
You can find full instruction in the [AWS IoT documentation](https://docs.aws.amazon.com/iot/latest/developerguide/create-device-certificate.html).
After downloading the certifactes, place them in [IoT/certs](IoT/certs) folder and update ```rootCAPath```, ```certificatePath``` and ```privateKeyPath``` in [IoT/watch_mqtt.py](IoT/watch_mqtt.py)

### End Point Setup
Each AWS IoT deployment has its own endpoint. Please update ```host``` variable in [IoT/watch_mqtt.py](IoT/watch_mqtt.py) to your specific endpoint.

## lambda
This folder includes the code running in AWS Lambda and triggered by AWS IoT button.
