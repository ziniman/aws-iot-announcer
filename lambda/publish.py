import json
import boto3
import logging
from datetime import datetime
from dateutil import tz

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from_zone = tz.gettz('UTC')
to_zone = tz.gettz('Asia/Jerusalem')

starts_in = {'SINGLE': 0,
    "DOUBLE": 2,
    "LONG": 5
}

client = boto3.client('iot-data', region_name='eu-west-1')

def lambda_handler(event, context):
    logger.info('Received event: ' + json.dumps(event))

    click_type = event["deviceEvent"]["buttonClicked"]["clickType"]
    event_timestamp = event["deviceEvent"]["buttonClicked"]["reportedTime"]
    device_id = event["placementInfo"]["devices"]["Announcer"]

    timestamp = datetime.utcnow()
    timestamp = timestamp.replace(tzinfo=from_zone)
    timestamplocal = timestamp.astimezone(to_zone)
    timelocal = int(timestamplocal.strftime('%H'))

    if timelocal<=12:
        day_part = 'morning'
    elif timelocal<=17:
        day_part = 'afternoon'
    else:
        day_part = 'evening'

    if starts_in[click_type]>1:
        session_start = "will start in %d minutes." % starts_in[click_type]
    else:
        session_start = "is starting now!"

    tts = ("Goog %s floor28 ateendees. Please join us at the main conference room. The session %s") % (day_part, session_start)
    logger.info(tts)
    # Change topic, qos and payload
    response = client.publish(
        topic='$aws/things/Floor28_RBPi/announce',
        qos=1,
        payload=json.dumps({"click":click_type,
            "timestamp": event_timestamp,
            "device_id": device_id,
            "tts": tts
        })
    )

    logger.info('IoT Response: ' + json.dumps(response))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
