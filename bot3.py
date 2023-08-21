# This example requires the 'message_content' privileged intent to function.
# Bot that starts a guessing game with $guess, shows messages that were edited and responds with a kissing emoji to 'petarda' or 'petardo'

import discord
import random
import asyncio
from dotenv import dotenv_values

# bot's token is hidden in .env and .gitignore
config = dotenv_values(".env")
token = config['TOKEN']

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        
        if message.content == 'petarda' or message.content == 'petardo':
            await message.add_reaction('\U0001F618')

        if message.content.startswith('$guess'):
            await message.channel.send('Guess a number between 1 and 10.')

            def is_correct(m):
                return m.author == message.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await self.wait_for('message', check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {answer}.')

            if int(guess.content) == answer:
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {answer}.')
                
    # client.event, checking if a message was edited
    async def on_message_edit(self, before, after):
        await before.channel.send(
            f'{before.author} edit a message. \n'
            f'Before: {before.content}\n'
            f'After: {after.content}'
        )


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)


