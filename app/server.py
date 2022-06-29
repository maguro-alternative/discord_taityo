from flask import Flask,request,jsonify
from threading import Thread
import requests
import os

app = Flask("")

@app.route("/", methods=["GET", "POST"])
def main():
	# LINEbotからpostリクエストが来た場合
	if request.method == 'POST':

		# 送られたjsonデータを展開
		json=request.get_json()


		# LINEbot側で設定されたサーバーIDと対象のテキストチャンネルIDを代入
		guild_id=int(json[0]["guild_id"])
		temple_id=int(json[0]["templeChannel_id"])
		
		# Discordbotのトークンとリクエストのリミットを宣言
		token=os.environ["TOKEN"]
		limit=os.environ["USER_LIMIT"]

		# リクエストヘッダ
		headers = {
        	'Authorization': f'Bot {token}',
			'Content-Type': 'application/x-www-form-urlencoded',
    	}

		# Discord側にWebリクエストをGETメゾットに送信
		response = requests.get(f'https://discordapp.com/api/guilds/{guild_id}/channels', headers=headers)

		# レスポンスコード表示(200で成功)
		print(response)

		# 受け取ったデータをjson形式で展開
		r = response.json()
		
		# メッセージにメンションが含まれている場合
		if json[0]["message"].find('@')>=0:
			# サーバーメンバーのデータを取得
			res = requests.get(f'https://discordapp.com/api/guilds/{guild_id}/members?limit={limit}', headers=headers)

			# データを展開しつつ該当するユーザーが存在するか探索
			for rs in res.json():
				if json[0]["message"].find(f'@{rs["user"]["username"]}')>=0:
					json[0]["message"]=json[0]["message"].replace(f'@{rs["user"]["username"]}',f'<@{rs["user"]["id"]}>')

			# サーバー内のロールを取得
			res = requests.get(f'https://discordapp.com/api/guilds/{guild_id}/roles', headers=headers)

			# データを展開しつつ該当するロールが存在するか探索
			for rs in res.json():
				if json[0]["message"].find(f'@{rs["name"]}')>=0:
					json[0]["message"]=json[0]["message"].replace(f'@{rs["name"]}',f'<@&{rs["id"]}>')

		# サーバー内のすべてのチャンネルを取得
		response = requests.get(f'https://discordapp.com/api/guilds/{guild_id}/channels', headers=headers)
		print(response)
		r = response.json()

		# メッセージの先頭に/が存在する場合
		if json[0]["message"].find('/')==0:
			for res in r:
				# テキストチャンネルの場合(type=0)
				if res["type"]==0:
					# print(f"{res['name']} {res['type']} {res['id']}")
					# テキストチャンネル名が存在する場合
					if json[0]["message"].find(f'/{res["name"]}')==0:
						json[0]["message"]=json[0]["message"].lstrip(f'/{res["name"]}')
						data = {"content":f'{json[0]["name"]}\n「 {json[0]["message"]} 」'}
						re=requests.post(f'https://discordapp.com/api/channels/{res["id"]}/messages', headers=headers, data=data)
		else:
			data = {"content":f'{json[0]["name"]}\n「 {json[0]["message"]} 」'}
			response = requests.post(f'https://discordapp.com/api/channels/{temple_id}/messages', headers=headers, data=data)  

		return "dmc"
	else:
		return "Hero is alive!"

def run():
  app.run("0.0.0.0", port=8080)
  #app.run()

def keep_alive():
  t = Thread(target=run)
  t.start()