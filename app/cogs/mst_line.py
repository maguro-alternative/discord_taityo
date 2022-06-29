import discord
import requests
import os

import json

from discord.ext import commands
from core.start import DBot

class mst_line(commands.Cog):
    def __init__(self, bot : DBot):
        self.bot = bot      

    # DiscordからLINEへ
    @commands.Cog.listener(name='on_message')
    async def on_message(self, message:discord.Message):
        #Google App ScriptのURL
        url=os.environ['GAS_URL']

        # botのメッセージはスキップ
        if message.author.bot is True:
            return

        # いかがわしいメッセージはスキップ
        if message.channel.nsfw is True:
            return

        # Google App Script(LINEbot)へ送るデータ
        jsonData={
                "events":[
                    {
                        "type": "discord",
                    }
                ]
        }
        """
        type:       discord
        channelname:discordのチャンネル名
        name:       discordのユーザー名
        message:    テキストメッセージ
        guildid:    サーバーid
        """
        jsonData["events"][0]={"type": "discord"}
        jsonData["events"][0]["channelname"]=message.channel.name
        jsonData["events"][0]["name"]=message.author.name
        jsonData["events"][0]["message"]=message.clean_content
        jsonData["events"][0]["guildid"]=str(message.guild.id)

        cnt=0
        
        # 送付ファイルありの場合画像か写真かで判断
        if message.attachments:
            jsonData["events"][0]["img"],cont=image_checker(message.attachments)
            cnt+=cont
            jsonData["events"][0]["video"],cont=video_checker(message.attachments)
            cnt+=cont

            # 画像や動画ではない場合メッセージにURLを貼り付ける
            if cnt<len(message.attachments):
                for attachment in message.attachments:
                    jsonData["events"][0]["message"]+=f"\n{attachment.url}"
            # jsonData["events"][0]["voice"]=voice_checker(message.attachments)
            
        # json形式に変換
        jsonData=json.dumps(jsonData)

        options = {
            "headers": json.dumps( { "Content-type": "application/json" })
        }

        # Google App Scriptにリクエストを送信
        r = requests.post(url=url ,data=jsonData, headers=options)

# 拡張子から画像ファイルか判断する
def image_checker(attachments):
    image=[".jpg",".png",".JPG",".PNG",".jpeg",".gif",".GIF"]
    eventsdata=[]
    cnt=0
    for attachment in attachments:
        for file in image:
            iurl=str(attachment.url)
            if iurl.endswith(file):
                eventsdata.append({f"image{cnt}": iurl})
                cnt+=1
   
    return eventsdata,cnt

# 拡張子から動画ファイルか判断する
def video_checker(attachments):
    video=[".mp4",".MP4",".MOV",".mpg",".avi",".wmv",".mpg"]
    eventsdata=[]
    cnt=0
    for attachment in attachments:
        for file in video:
            iurl=str(attachment.url)
            if iurl.endswith(file):
                eventsdata.append({f"video{cnt}": iurl})
                cnt+=1
   
    return eventsdata,cnt

def voice_checker(attachments):
    voice=[".wav",".mp3",".flac",".aif",".m4a",".oga",".ogg"]
    eventsdata=[]
    cnt=0
    for attachment in attachments:
        for file in voice:
            iurl=str(attachment.url)
            if iurl.endswith(file):
                eventsdata.append({f"voice{cnt}": iurl})
                cnt+=1
   
    return eventsdata

def setup(bot):
    return bot.add_cog(mst_line(bot))