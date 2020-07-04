#coding: UTF-8
import os
import slack
import datetime
import time
from dateutil.relativedelta import relativedelta
from logging import getLogger,StreamHandler,Formatter,DEBUG,INFO,WARNING,ERROR,CRITICAL

logger = getLogger(__name__)
logger.setLevel(DEBUG)
loghandler = StreamHandler()
loghandler.setFormatter(Formatter("%(asctime)s %(name)s %(levelname)8s %(message)s"))
logger.addHandler(loghandler)

logger.info('Start processing.')
client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
post_channel = os.environ['POST_CHANNEL']
logger.info('Successfully read environmental variables.')

ABEND_ERROR_TIMES = 10

def create_new_channel() -> str:
    logger.info('Start create channel process.')
    
    message = 'エラーが発生しました'
    dt_now = datetime.datetime.now()
    new_channel_name = datetime.datetime.strftime(dt_now + relativedelta(months=1), '%Y-%m')
    conversations_list = client.conversations_list()
    assert conversations_list['ok'],'チャンネル一覧の取得に失敗しました'
    logger.info('Successfully got channel list.')


    is_channel_exists = False
    channels = conversations_list['channels'] 
    for channel in channels:
        if channel['name'] == new_channel_name:
            logger.info('#' + new_channel_name + ' is searched.')
            is_channel_exists = True
            break

    if is_channel_exists == True:
        logger.info('#' +new_channel_name + ' is already exists.')
        message = '#' + new_channel_name + 'は作成済みだよー'
    else:
        logger.info(new_channel_name + ' is not exists. Start creating.')
        new_channel = client.channels_create(name=new_channel_name)
        assert new_channel['ok'],'チャンネルの作成に失敗しました'
        logger.info(new_channel_name + ' is created.')
        message = '#' + new_channel_name + 'を作成したよー'
        
        users_list = client.users_list()
        logger.info('Successfully got userlist.')
        assert users_list['ok'],'ユーザー一覧の取得に失敗しました'
        
        users = users_list['members']
        exec_user_id = os.environ['EXEC_USER_ID']

        err_times = 0
        for user in users:
            try:
                invite(user)
                time.sleep(1)
            except:
                err_times += 1
                logger.info('Failed to invite'+ user['id'] + ':' + user['name'] + '.')
                if err_times > ABEND_ERROR_TIMES:
                    break
                pass
    
    logger.info('Finish create channel process.')
    return message
    
def invite(user):
    logger.info('Going to invite'+ user['id'] + ':' + user['name'] + '.')
    #自分自身は招待しない
    if user['id'] == exec_user_id:
        logger.info('myself.')
        return
    #botは招待しない
    if user['is_bot'] == True:
        logger.info('is_bot.')
        return
    #updated=0は招待しない エラーになる理由はわからない
    if user['updated'] == 0:
        logger.info('updated equal 0.')
        return
            
    #チャンネルに招待
    dt_now = datetime.datetime.now()
    
    ret = client.channels_invite(channel=new_channel['channel']['id'],user=user['id'])
    logger.info('Invited'+ user['id'] + ':' + user['name'] + '.')
    assert ret['ok'],'ユーザーの招待に失敗しました' + '(' + user['name'] + ')'

if __name__ == "__main__":
    create_new_channel()