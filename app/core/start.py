import discord
import os
import traceback

class DBot(discord.AutoShardedBot):
    def __init__(self, token, intents):
        self.token = token
        super().__init__(intents = intents)
        self.load_cogs()

    async def on_ready(self):
        print('起動しました')
        await self.change_presence(activity=discord.Game(name="senran kagura"))

    def load_cogs(self):
        for file in os.listdir("./cogs"): 
            if file.endswith(".py"): 
                cog = file[:-3] 
                self.load_extension(f"cogs.{cog}")
                print(cog + "をロードしました")

    # 起動用の補助関数
    def run(self):
        try:
            self.loop.run_until_complete(self.start(self.token))
        except discord.LoginFailure:
            print("Discord Tokenが不正です")
        except KeyboardInterrupt:
            print("終了します")
            self.loop.run_until_complete(self.logout())
        except:
            traceback.print_exc()