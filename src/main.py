#coding: UTF-8
import os
import slack
import datetime
import time
from dateutil.relativedelta import relativedelta
from logging import getLogger,StreamHandler,Formatter,DEBUG,INFO,WARNING,ERROR,CRITICAL
import src.create_new_channel as create_new_channel
import src.archive_old_channels as archive_old_channels

logger = getLogger(__name__)
logger.setLevel(DEBUG)
loghandler = StreamHandler()
loghandler.setFormatter(Formatter("%(asctime)s %(name)s %(levelname)8s %(message)s"))
logger.addHandler(loghandler)

logger.info('Start processing.')
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
post_channel = os.environ['POST_CHANNEL']
logger.info('Successfully read environmental variables.')

def handler(event, lambda_context):
    try:
        message_create = create_new_channel.create_new_channel()
        client.chat_postMessage(channel=post_channel, text=message_create)
        message_archive = archive_old_channels.archive_old_channels()
        client.chat_postMessage(channel=post_channel, text=message_archive)
        logger.info('Finish processing.')

    except Exception as e:
        logger.error('An Error has occurred.')
        message_error = "エラーが発生しました"
        client.chat_postMessage(channel=post_channel, text=message_error)
        raise e 
