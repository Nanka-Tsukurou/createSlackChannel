# createSlackChannel
[処理概要]

・チャンネル（#YYYY-MM）を新規作成

・ワークスペースの全参加者をjoin

・3か月以上前の#YYYY-MMをアーカイブ

[実行方法]

・毎月1日の定期実行

・slack上でスラッシュコマンドによる手動実行も可能
```
/createchannel
```
[デプロイ]
※AWSのアカウントを持っていて、アクセスキーを取得していること
※slackのAPPを作成済みであること

1.git clone

2.AWS S3バケットを作成（任意の名前）

3./createSlackChannel/myCustomfile.ymlを作成し、以下を記載
```
slack_token: <slackのトークン>
post_chennel_prod: <＃実行結果を通知するslackのチャンネル名>
exec_user_id_prod: <slackの実行ユーザーID>
deployment_bucket: <2.で作成したS3バケットの名前>
```

4./createSlackChannel直下で以下コマンドを実行
```
sls deploy -v
```

5.POSTのエンドポイントを、slackAPPのスラッシュコマンドの"Request URL"に記載


