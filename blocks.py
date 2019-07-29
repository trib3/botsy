LEARN_OR_TEACH = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "Hi! I'm *Botsy*! Would you like to *learn* or *teach*?"
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Learn"
                },
                "value": "learnBlock"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Teach"
                },
                "value": "teachBlock"
            }
        ]
    }
]

TEACH_FORM = {
    "title": "Teach",
    'callback_id': 'teach_dialog04435',
    "submit_label": "Submit",
    "state": "Teach",
    'elements':
        [
            {'name': 'teach_topic',
            'label': 'What topic would you like to teach?',
            'type': 'text',
            'placeholder': 'Cats!'}
            ]
}

LEARN_FORM = {
    "title": "Learn",
    'callback_id': 'learn_dialog04435',
    "submit_label": "Submit",
    "state": "Learn",
    'elements':
        [
            {'name': 'learn_topic',
            'label': 'What topic would you like to learn about?',
            'type': 'text',
            'placeholder': 'Cats!'}
            ]
}


def generate_teacher_request_block(topic):
    return [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hi <!channel>! Can anyone help teach *{topic}*? We've got someone who wants to learn."
        }
    },
    {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "I Can!"
                },
                "value": f"volunteerBlock__{topic}"
            }
        ]
    }
]


def generate_join_block(topic, teacher):
    return [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"Hi! Who wants to learn about *{topic}*? @{teacher} wants to teach! Please emoji if you're interested, and we'll get you connected."
        }
    }
]