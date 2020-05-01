#coding: UTF-8
import os
import slack
import datetime
import time
from dateutil.relativedelta import relativedelta
import logging
import archive_old_channels
import create_new_channel

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

logging.info('Start processing.')
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
post_channel = os.environ['POST_CHANNEL']
logging.info('Successfully read environmental variables.')

def handler(event, lambda_context):
    try:
        message_create = create_new_channel.create_new_channel(client)
        client.chat_postMessage(channel=post_channel, text=message_create)
        message_archive = archive_old_channels.archive_old_channels(client)
        client.chat_postMessage(channel=post_channel, text=message_archive)
        logging.info('Finish processing.')

    except Exception as e:
        logging.error('An Error has occurred.')
        raise e 
        
if __name__ == "__main__":
    handler('event', 'lambda_context')
