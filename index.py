import json
import re
import os
import logging
import urllib.parse

from blocks import (
    LEARN_OR_TEACH,
    TEACH_FORM,
    LEARN_FORM,
    generate_teacher_request_block,
    generate_join_block
)
from api import (
    create_channel,
    invite_to_channel,
    unarchive_channel,
    get_channel,
    delete_message,
    get_message,
    channel_message,
    ephemeral_message,
    create_dialog,
    respond
)
from helper_functions import verify_signature, generate_channel_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LEARNINGS_CHANNEL = os.environ.get('LEARNINGS_CHANNEL')
BOT_ID = os.environ.get('BOT_ID')


def handler(event, context):
    if 'payload' in event['body']:
        if not verify_signature(event):
            return respond('Unauthorized user.')

        payload = urllib.parse.parse_qs(event['body'])
        data = json.loads(payload['payload'][0])
        payload_type = data['type']

        if payload_type == 'block_actions':
            value = data['actions'][0]['value']
            trigger_id = data['trigger_id']
            if value == 'teachBlock' or value == 'learnBlock':
                form = TEACH_FORM if value == 'teachBlock' else LEARN_FORM
                create_dialog(trigger_id, form)

            # Someone clicked "I can" to volunteer to teach a topic
            elif 'volunteerBlock' in value:
                user_name = data['user']['username']
                user = data['user']['id']
                topic = value.split('__')[-1]
                blocks = generate_join_block(topic, user_name)
                channel_message(LEARNINGS_CHANNEL, blocks)
                ts = data['message']['ts']
                # Delete the original message requesting volunteer so we don't
                # get multiple volunteers
                delete_message(LEARNINGS_CHANNEL, ts)
                create_channel(topic, user)

        if payload_type == 'dialog_submission':
            state = data['state']
            user_name = data['user']['name']
            user = data['user']['id']
            # State someone has volunteered to teach a topic
            if state == 'Teach':
                topic = data['submission']['teach_topic']
                blocks = generate_join_block(topic, user_name)
                channel_message(LEARNINGS_CHANNEL, blocks)
                create_channel(topic, user)
            # Request someone to teach topic
            else:
                topic = data['submission']['learn_topic']
                blocks = generate_teacher_request_block(topic)
                channel_message(LEARNINGS_CHANNEL, blocks)
        return respond(None, res={})

    else:
        data = json.loads(event['body'])
        if data['type'] == 'url_verification':
            return respond(None, res=data)
        elif not verify_signature(event):
            return respond('Unauthorized user.')

        event_info = data['event']
        if "bot_id" in event_info:
            logging.warn("Ignore bot event")
        else:
            event_type = event_info["type"]

            if event_type == 'app_mention' or event_type == 'message':
                get_channel('botsy-learnings')
                channel_id = event_info["channel"]
                user = event_info["user"]
                ephemeral_message(channel_id, user, LEARN_OR_TEACH)
            elif event_type == 'reaction_added':
                user = event_info['user']
                ts = event_info['item']['ts']
                channel = event_info['item']['channel']

                # Now we need to retrieve which post was reacted to
                message_dict = get_message(channel, ts)

                # If the message the user responded to was posted by our bot
                if message_dict['bot_id'] == BOT_ID:
                    topic = re.search('\*(.*)\*', message_dict['text']).group(1)
                    channel_name = generate_channel_name(topic)
                    channel_exists = get_channel(channel_name)

                    # If there is a channel, add the user to that channel
                    if channel_exists:
                        # if the channel is archived, then unarchive it first
                        if channel_exists['is_archived']:
                            unarchive_channel(channel_exists['id'])
                        invite_to_channel(channel_exists['id'], user)
                    else:
                        print('no channel exists sorry')

    return respond(None, res=data)


