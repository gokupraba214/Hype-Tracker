from twitchio.ext import commands
import asyncio

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token='anonymous', prefix='?', initial_channels=['ninja'])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return
        print(f"[{message.channel.name}] {message.author.name}: {message.content}")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot = Bot()
    loop.run_until_complete(bot.start())
