# aws-iot-announcer
A simple app that is using a RaspberryPi device controlled by an AWS IoT Button to play public announcment using Amazon Polly as the TTS engine.

## IoT
This folder includes the code running on the RaspberryPi device.

### IoT Requirements
This part of the app is running on a RaspberryPi (Tested on Model B+ and above) and require the following components to run the code:

#### AWS CLI
The AWS CLI is an open source tool that provides commands for interacting with AWS services. With minimal configuration, you can start using all of the functionality provided by the AWS Management Console from your favorite terminal program.
AWS CLI will allow you to define your user credentilas to access your AWS account and invoke different services. In our case, we need access to AWS Polly (Text to speech Service) to convert the announcments into sound files.

```
pip install awscli --upgrade --user
```

#### boto3
[Boto](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) is the Amazon Web Services (AWS) SDK for Python, which allows Python developers to write software that makes use of Amazon services like S3, EC2 and IoT. You will need to install boto3 using the next command.

```
pip install boto3
```
After installation, please follow these [instruction](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) to configure your enviournment.

#### AWSIoTMQTTClient
The AWS IoT Device SDK for Python allows developers to write Python script to use their devices to access the AWS IoT platform through MQTT or MQTT over the WebSocket protocol.
```
pip install AWSIoTPythonSDK
```
For setup and configuration details check the [github repository](https://github.com/aws/aws-iot-device-sdk-python).

## lambda
This folder includes the code running in AWS Lambda and triggered by AWS IoT button.
