import os
from src import amplify_slack_notifications

# Env vars:
# * HOOK_URL     = os.environ['WebhookUrl']
# * MAIN_URL     = os.environ['MainUrl']
# * DEV_URL      = os.environ['DevUrl']
# * FALLBACK_URL = os.environ['FallbackUrl']


TEST_EVENT = {
    "Records": [
        {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:eu-central-1:123456789012:amplify-d175k12vz3k144_main:8879aad1-28a7-4bf5-b724-d3a26642d2ac",
            "Sns": {
                "Type": "Notification",
                "MessageId": "ec7f0492-4cab-5c55-8e9d-5fab5bb0fd4b",
                "TopicArn": "arn:aws:sns:eu-central-1:123456789012:amplify-d175k12vz3k144_main",
                "Subject": "None",
                "Message": "'Build notification from the AWS Amplify Console for app: https://main.d175k12vz3k144.amplifyapp.com/. Your build status is SUCCEED. Go to https://console.aws.amazon.com/amplify/home?region=eu-central-1#d175k12vz3k144/main/99 to view details on your build. '",
                "Timestamp": "2022-07-01T15:38:03.346Z",
                "SignatureVersion": "1",
                "Signature": "ISUyWquFzpe4nL+tsGJTM2JH0u0uzyZwIlysczWIHPCvT4XrJzjhWq2Qa6rwOme7M5SRDRy6uYzjHFr+qqPof4Q3Ve0KYtlFYnzdxM8Qxj+e6OMsO5Hmnt7ilvSGPlKEx6j7z0ZjETKoazgc6ER/cb/cHgNsPHZU4DEljzxjHVmXljBzpn38qWBGhxAnzLAKScD3HHbAAI0bXrHnGzr9ybBl5Us01ZSkA/KttmDfRDe0zOHFMapXiKpXAmlbUH46xmrI/a7qJe5di0UrjxaVWpmEt9JDMKA9aFHFA7q4Sa1fR8HJeZMmRNrIsCO+bcvIMEhvupmBIO4Ee2SpwSf1cw==",
                "SigningCertUrl": "https://sns.eu-central-1.amazonaws.com/SimpleNotificationService-7ff5318490ec183fbaddaa2a969abfda.pem",
                "UnsubscribeUrl": "https://sns.eu-central-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:eu-central-1:123456789012:amplify-d175k12vz3k144_main:8879aad1-28a7-4bf5-b724-d3a26642d2ac",
                "MessageAttributes": {}
            }
        }
    ]
}

BUILT_SLACK_MESSAGE = {
    "attachments": [
        {
            "fallback": "Amplify Build Status",
            "color": "#00ff00",
            "author_name": f"Amplify Build Status: SUCCEED",
            "fields": [
                {"title": "Account", "value": "123456789012", "short": "false"},
                {"title": "Region", "value": "eu-central-1", "short": "false"},
                {
                    "title": "Event time (UTC)",
                    "value": "2022-07-01 15:38:03.346",
                    "short": "false",
                },
                {"title": "App", "value": "d175k12vz3k144", "short": "false"},
            ],
            "footer": "globaldatanet",
            "ts": 1655379128889,  # TimeStamp for last update
            "actions": [
                {
                    "type": "button",
                    "text": {"type": "Open in AWS", "text": "Link Button"},
                    "url": "https://eu-central-1.console.aws.amazon.com/amplify/#/d175k12vz3k144",
                }
            ],
        }
    ]
}


def test_setting_data():
    '''
    GIVEN: event received
    WHEN: Amplify build triggered SNS event
    THEN: set data accordingly
    '''

    slack_message = amplify_slack_notifications.build_message_data(TEST_EVENT, {})
    assert slack_message == BUILT_SLACK_MESSAGE


def test_send_slack_message():
    '''
    GIVEN: configured slack message
    WHEN: sending to slack
    THEN: status is 200 OK
    '''

    event = TEST_EVENT
    context = None

    payload = amplify_slack_notifications.handler(event, context)
    assert payload['statusCode'] == 200


def test_set_status_color():
    '''
    GIVEN: Status from SNS event
    WHEN: SUCCEED | STARTED | FAILED
    THEN: green | blue | red
    '''

    for status in ['SUCCEED', 'STARTED', 'FAILED']:

        if status == 'SUCCEED':
            assert amplify_slack_notifications.set_status_color(status) == "#00ff00"

        if status == 'STARTED':
            assert amplify_slack_notifications.set_status_color(status) == "#00bbff"

        if status == 'FAILED':
            assert amplify_slack_notifications.set_status_color(status) == "#ff0000"

        if status is None:
            assert amplify_slack_notifications.set_status_color(status) == "#808080"
