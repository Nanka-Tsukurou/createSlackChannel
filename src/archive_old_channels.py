#coding: UTF-8
import slack
import datetime
import time
from dateutil.relativedelta import relativedelta
from logging import getLogger,StreamHandler,Formatter,DEBUG,INFO,WARNING,ERROR,CRITICAL
import re

logger = getLogger(__name__)
logger.setLevel(DEBUG)
loghandler = StreamHandler()
loghandler.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))
logger.addHandler(loghandler)

def archive_old_channels(client) -> str:
    logger.info('Start archive process.')

    dt_now = datetime.datetime.now()
    new_channel_name = datetime.datetime.strftime(dt_now + relativedelta(months=1), '%Y-%m')
    conversations_list = client.conversations_list()
    assert conversations_list['ok'],'チャンネル一覧の取得に失敗しました'

    pattern = '#\d{4}-\d{2}' #YYYY-MM形式
    channels = conversations_list['channels']

    message = 'アーカイブ対象はありませんでした'
    for channel in channels:
        archive_channel_name = channel['name']
        archive_channel_id = channel['id']
        is_archived = channel['is_archived']

        if (re.fullmatch(pattern,archive_channel_name) is not None) and (not is_archived):#YYYY-MM形式にマッチ、かつ、未アーカイブ
            dt_archive_channel = datetime.datetime.strptime(archive_channel_name, '%Y-%m')
            logger.info('channel name :' + archive_channel_name + 'is matched.')
            #実行時の3ヶ月前より前はアーカイブ
            #2020-01は、2020/04/01起動時にアーカイブされる
            if dt_archive_channel.replace(day=1,hour=0,minute=0,second=0,microsecond=0) + relativedelta(months=3) < dt_now:
                logger.info('channel name :' + archive_channel_name + 'will be archived.')
                client.conversations_archive(channel=archive_channel_id)
                assert conversations_list['ok'],'チャンネルのアーカイブに失敗しました'
                logger.info('Channel' + archive_channel_name + 'has been archived.')
                message = archive_channel_name + 'をアーカイブしたよー'

    logger.info('Finish archive process.')
    return message

if __name__ == "__main__":
    archive_old_channels()
        
    
