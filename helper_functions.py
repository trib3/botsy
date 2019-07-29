import time
import hmac
import hashlib
import os

SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')


def generate_channel_name(topic):
    topic = str(topic).lower().replace(' ', '-').replace('.', '-')
    if len(topic) > 21:
        topic = topic[:21]
    return f'{topic}-learnings' if len(f'{topic}-learnings') < 22 else topic


def verify_signature(event):
    """
    Returns true if the signature is correct and from slack, false otherwise
    """
    slack_signature = event['headers']['X-Slack-Signature']
    timestamp = event['headers']['X-Slack-Request-Timestamp']
    body = event['body']
    if abs(time.time() - int(timestamp)) > 60 * 5:
        # The request timestamp is more than five minutes from local time.
        # It could be a replay attack, so let's ignore it.
        return False

    sig_basestring = 'v0:' + timestamp + ':' + event['body']
    my_signature = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)