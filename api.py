import os
import json
import requests

from helper_functions import generate_channel_name

CREATOR_ID = os.environ.get('CREATOR_ID')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
SLACK_OAUTH_TOKEN = os.environ.get('SLACK_OAUTH')

SLACK_CHAT_POST_API_EPHEMERAL = 'https://slack.com/api/chat.postEphemeral'
SLACK_CHAT_POST_API_PUBLIC = 'https://slack.com/api/chat.postMessage'
SLACK_DIALOG_POST_API = 'https://slack.com/api/dialog.open'
SLACK_DELETE_MESSAGE_API = 'https://slack.com/api/chat.delete'
SLACK_CHANNEL_HISTORY_API = 'https://slack.com/api/channels.history'
SLACK_CHANNEL_INVITE_API = 'https://slack.com/api/conversations.invite'
SLACK_CONVERSATIONS_LIST = 'https://slack.com/api/conversations.list'
SLACK_CONVERSATIONS_CREATE = 'https://slack.com/api/conversations.create'
SLACK_CONVERSATIONS_LEAVE = 'https://slack.com/api/conversations.leave'
SLACK_CONVERSATIONS_JOIN = 'https://slack.com/api/conversations.join'
SLACK_CONVERSATIONS_UNARCHIVE = 'https://slack.com/api/conversations.unarchive'

"""
*****************
Channels
*****************
"""


def create_channel(topic, user):
    channel_name = generate_channel_name(topic)
    channel_exists = get_channel(channel_name)

    # If there is a channel, add the teacher to that channel
    if channel_exists:
        channel_id = channel_exists['id']
    # If there is no existing channel, create a new one
    else:
        response = requests.post(SLACK_CONVERSATIONS_CREATE, data={
            'token': SLACK_OAUTH_TOKEN,
            'name': channel_name,
            'is_private': False,
        }).json()

        if 'channel' in response:
            channel_id = response['channel']['id']
        else:
            # TODO: error dialog
            return respond(None, res={})

    invite_to_channel(channel_id, user)

    # Kick myself out of the channel unless I prompted creation
    if user != CREATOR_ID:
        leave_channel(channel_id)


def invite_to_channel(channel_id, user_id):
    if user_id == CREATOR_ID:
        response = requests.post(SLACK_CONVERSATIONS_JOIN, data={
            'token': SLACK_OAUTH_TOKEN,
            'channel': channel_id
        })
    else:
        response = requests.post(SLACK_CHANNEL_INVITE_API, data={
            'token': SLACK_OAUTH_TOKEN,
            'channel': channel_id,
            'users': user_id
        })


def leave_channel(channel_id):
    response = requests.post(SLACK_CONVERSATIONS_LEAVE, data={
        'token': SLACK_OAUTH_TOKEN,
        'channel': channel_id
    })


def unarchive_channel(channel):
    response = requests.post(SLACK_CONVERSATIONS_UNARCHIVE, data={
        'token': SLACK_OAUTH_TOKEN,
        'channel': channel
    }).json()


def get_channel(channel_name):
    response = requests.get(SLACK_CONVERSATIONS_LIST, params={
        'token': SLACK_OAUTH_TOKEN,
        'limit': 1000,
        'types': 'public_channel,private_channel'
    }).json()
    channels = response['channels']

    channel_match = next((channel for channel in channels if
                          channel["name"] == channel_name), None)

    return channel_match


"""
*****************
Messages
*****************
"""


def channel_message(channel_id, blocks='', text=''):
    requests.post(SLACK_CHAT_POST_API_PUBLIC, data={
        'token': BOT_TOKEN,
        'channel': channel_id,
        'text': text,
        'blocks': json.dumps(blocks),
    })


def delete_message(channel_id, ts):
    requests.post(SLACK_DELETE_MESSAGE_API, data={
        'token': BOT_TOKEN,
        'channel': channel_id,
        'ts': ts
    })


def get_message(channel, timestamp):
    # use SLACK_CHANNEL_HISTORY_API once this is public
    message = requests.get(SLACK_CHANNEL_HISTORY_API, params={
        'token': SLACK_OAUTH_TOKEN,
        'channel': channel,
        'count': 1,
        'latest': timestamp,
        'inclusive': True
    }).json()

    return {
        'bot_id': message['messages'][0]['bot_id'],
        'text': message['messages'][0]['blocks'][0]['text']['text']
    }


def ephemeral_message(channel_id, user, blocks='', text=''):
    requests.post(SLACK_CHAT_POST_API_EPHEMERAL, data={
        'token': BOT_TOKEN,
        'channel': channel_id,
        'text': text,
        'blocks': json.dumps(blocks),
        'user': user
    })


"""
*****************
Dialogs
*****************
"""


def create_dialog(trigger_id, form):
    requests.post(SLACK_DIALOG_POST_API, data={
        'token': SLACK_OAUTH_TOKEN,
        'trigger_id': trigger_id,
        'dialog': json.dumps(form)
    }).json()


"""
*****************
Misc
*****************
"""


def respond(err, res=None, challenge=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
