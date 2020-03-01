import os
import slack
import datetime
import time
from dateutil.relativedelta import relativedelta
from logging import getLogger

logger = getLogger(__name__)

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
post_channel = os.environ['POST_CHANNEL']
message = 'エラーが発生しました'

def create_new_channels():
    dt_now = datetime.datetime.now()
    new_channel_name =  datetime.datetime.strftime(dt_now + relativedelta(months=1), '%Y-%m')
    conversations_list = client.conversations_list()
    assert conversations_list['ok'],'チャンネル一覧の取得に失敗しました'

    is_channel_exists = False
    channels = conversations_list['channels'] 
    for channel in channels:
        if channel['name'] == new_channel_name:
            is_channel_exists = True
            break

    if is_channel_exists == True:
        message = '#' + new_channel_name + 'は作成済みだよー'
    else:
        message = '#' + new_channel_name + 'を作成したよー'
        new_channel = client.channels_create(name=new_channel_name)
        assert new_channel['ok'],'チャンネルの作成に失敗しました'

        users_list = client.users_list()
        assert users_list['ok'],'ユーザー一覧の取得に失敗しました'
        
        users = users_list['members']
        for user in users:
            
            exec_user_id = os.environ['EXEC_USER_ID']
            #自分自身は招待しない
            if user['id'] == exec_user_id:
                continue
            #botは招待しない
            if user['is_bot'] == True:
                continue
            #updated=0は招待しない エラーになる理由はわからない
            if user['updated'] == 0:
                continue
            
            #チャンネルに招待
            dt_now = datetime.datetime.now()
            time.sleep(1)
            
            ret = client.channels_invite(channel=new_channel['channel']['id'],user=user['id'])
            assert ret['ok'],'ユーザーの招待に失敗しました' + '(' + user['name'] + ')'
                        
    client.chat_postMessage(channel=post_channel, text=message)

def handler(event, lambda_context):
    try:
        create_new_channels()

    except Exception as e:
        logger.exception('fail')

        raise e 
        
if __name__ == "__main__":
    create_new_channels()
