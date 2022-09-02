import os
import re
import json
import logging
import requests

# TODO:
# * Dynamic epoch for last updated timestamp

HOOK_URL     = os.environ['WebhookUrl']
MAIN_URL     = os.environ['MainUrl']
DEV_URL      = os.environ['DevUrl']
FALLBACK_URL = os.environ['FallbackUrl']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event: dict, _: dict) -> None:
    '''
        Lambda entrypoint
    '''

    logger.info(f'Received event: {event}')

    message = build_message_data(event)
    send_slack_message(message)


def build_message_data(event: dict) -> dict:
    '''Builds message for Slack in JSON format

    Args:
        event (dict): Incoming AWS event (SNS)

    Returns:
        dict: Slack message (JSON)
    '''

    sns_topic_arn = event['Records'][0]['Sns']['TopicArn']

    # Needed to deconstruct
    timestamp  = re.split('T|Z', event['Records'][0]['Sns']['Timestamp'])
    arn_string = re.findall(r'arn:aws:sns:(\S+):', sns_topic_arn)[0].split(':')


    # * Structure data from event
    status         = re.findall(
        r'Your build status is (\w+)+', event['Records'][0]['Sns']['Message']
    )[0]
    aws_region           = arn_string[0]
    aws_account_id       = arn_string[1]
    event_time_timestamp = timestamp[1]
    event_time           = f'{timestamp[0]} {event_time_timestamp[:-4]}'
    app_env              = re.search(r'arn:aws:sns:[\S]+:amplify-[\S]+_(\S+)', sns_topic_arn).group(1)
    amplify_id           = re.search(r'arn:aws:sns:[\S]+:amplify-(\S+)_', sns_topic_arn).group(1)
    amplify_build_url    = f'https://{aws_region}.console.aws.amazon.com/amplify/#/{amplify_id}'

    if app_env == 'main':
        open_url = MAIN_URL
    elif app_env == 'dev':
        open_url = DEV_URL
    else:
        open_url = FALLBACK_URL

    # Helps debugging
    logger.info(
        f'''Setting variables:\n
        Status: {status}\n
        App Env: {app_env}\n
        AWS Account ID: {aws_account_id}\n
        AWS Region: {aws_region}\n
        Event time: {event_time}\n
        URL: {open_url}
        '''
    )

    color = set_status_color(status)


    # Build message data
    message_data = {
        'attachments': [
            {
                'fallback': 'Amplify Build Status',
                'color': color,
                'author_name': f'Amplify Build Status: {status}',
                'fields': [
                    {'title': 'Account', 'value': aws_account_id, 'short': 'false'},
                    {'title': 'Region', 'value': aws_region, 'short': 'false'},
                    {
                        'title': 'Event time (UTC)',
                        'value': event_time,
                        'short': 'false',
                    },
                    {'title': 'Env', 'value': app_env, 'short': 'false'},
                ],
                'footer': 'globaldatanet',
                'ts': 1655379128889,  # TimeStamp for last update
                'actions': [
                    {
                        'type': 'button',
                        'text': {'type': 'Open live URL', 'text': 'Link Button'},
                        'url': open_url,
                    }
                ],
            }
        ]
    }

    # Add additional button in case Amplify build fails
    if status == 'FAILED':
        message_data['attachments'][0]['actions'] += [{
            'type': 'button',
            'text': {'type': 'Open Amplify build', 'text': 'Link Button'},
            'url': amplify_build_url,
        }]

    return message_data


def set_status_color(status: str) -> str:
    '''Sets color for slack message side bar

    Args:
        status (str): Status of Amplify build

    Returns:
        str: HEX color code
    '''

    # Set the color depending on status/category
    if status == 'SUCCEED':
        color = '#00ff00'  # green
    elif status == 'STARTED':
        color = '#00bbff'  # blue
    elif status == 'FAILED':
        color = '#ff0000'  # red
    else:
        color = '#808080'

    return color

def send_slack_message(message: dict) -> None:
    '''_summary_

    Args:
        message (dict): Slack message in JSON format
    '''

    try:
        logger.info('Sending message to slack...')
        requests.post(HOOK_URL, json.dumps(message))

    except Exception as error:
        logger.error(f'An error occured: {error}')

    else:
        logger.info('Successfully sent message')
