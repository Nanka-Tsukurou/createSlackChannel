#coding: UTF-8
import os
import slack
import datetime
import time
from dateutil.relativedelta import relativedelta
from logging import getLogger,StreamHandler,Formatter,DEBUG,INFO,WARNING,ERROR,CRITICAL
import src.create_new_channel as create_new_channel
import src.archive_old_channels as archive_old_channels
import requests
import json

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
    if 'body' in event: #スラッシュコマンドで呼ばれた場合
        logger.info('This process is kicked by a slash command.')
        response_url = event['body']['response_url']
        response_headers = {'content-type': 'application/json'}
    else: #定期実行で呼ばれた場合
        logger.info('This process is kicked by a cron job.')
    
    try:
        message_create = create_new_channel.create_new_channel()
        client.chat_postMessage(channel=post_channel, text=message_create)
        message_archive = archive_old_channels.archive_old_channels()
        client.chat_postMessage(channel=post_channel, text=message_archive)
        
        logger.info('Response will be sent.')
        logger.debug('responseurl:'+ response_url)

        #リクエストに、処理成功を返す(実際は先にレスポンスを返しているので、リクエストを別に送っている)
        payload = {
            'response_type':'ephemeral',
            'text':'success!'
        }
        r = requests.post(response_url, data=json.dumps(payload), headers=response_headers)
        logger.debug("response:" + str(r.status_code) + ":" + r.text)
        
        logger.info('Response has been sent.')
        logger.info('Finish processing.')

    except Exception as e:
        logger.error('An Error has occurred.')
        message_error = "エラーが発生しました"
        client.chat_postMessage(channel=post_channel, text=message_error)

        #リクエストに、エラーを返す(実際は先にレスポンスを返しているので、リクエストを別に送っている)
        payload_error = {
            'response_type':'ephemeral',
            'text':'error!'
        }
        er = requests.post(response_url, data=json.dumps(payload_error), headers=response_headers)
        logger.debug("error_response:" + str(er.status_code) + ":" + er.text)

        logger.info('Error Response has been sent.')
        raise e 
