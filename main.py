############################################################
### 1. Environment Setup
############################################################
import os
from discord.ext import commands
import discord

from dotenv import load_dotenv, find_dotenv
load_dotenv()  # take environment variables from .env.

############################################################
### 2. Bot Setup
############################################################
#client = discord.Client(intents=discord.Intents.default())
##### I had to change it to this in order to get it to see when members join
intents = discord.Intents.default()
intents.message_content = True

intents=discord.Intents.all()
#client = commands.Bot(command_prefix=',', intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


############################################################
### 3. Actual Bot Code
############################################################
@bot.event
async def on_ready():
    print("2nd branch called on ready")
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    
    
############################################################
### 4. Basic Checkup - on_message toolkit
############################################################
@bot.event
async def on_message(message):
    print("2nd branch called on_message")
    if message.author == bot.user:
        return
    #### Basic Ping
    if message.content.startswith('hello'):
        await message.channel.send('and to you to')
    #### Private DM
    if message.content.startswith('feedback'):
        c = await message.author.create_dm()
        await c.send(message.content)
    ####
    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    if message.content.startswith('!welcome'):
            with open('images/Workshopassistant.jpeg', 'rb') as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
                await message.channel.send('**Hello World! I am Workshop Assistant** ')
                await message.channel.send("\"_Sometimes the smallest things make the biggest difference._\" ")
                await message.channel.send('- Greet New Members (!welcome)')
                await message.channel.send('- Fetch Tech-Related News (!news)')
                await message.channel.send('- Scheduler (Repeated Events)')
                await message.channel.send('- Remind you the Day and the Date (!clock)')
                await message.channel.send('- Send LoFi Vibes (!lofi)')

    if message.content.startswith('!news'):
        await message.channel.send("**Cyber-Related News Bytes For Today Are As Follows: **\nKeep in mind these are the tweets from @bleepingcomputer, let me know if you have a preferred twitter account to scrape!")
      
        for i in tweets:
            minimalTitleText = i.text
            expanded_url = i.entities["urls"][0]["expanded_url"]
            createdDate = i._json["created_at"]
#           await message.channel.send(minimalTitleText)
#            await message.channel.send("**Tweet #%s**" % i)
            await message.channel.send(".")

            await message.channel.send("--------------------------------------------------------\n**Date Posted: %s**\n--------------------------------------------------------\n" % createdDate)
            await message.channel.send(expanded_url)

           # await message.channel.send("**Cyber-Related NewsBytes for Today Are as Follows:::**\nKeep in mind these are the tweets from @bleepingcomputer, let me know if you have a preferred twitter account to scrape!")
          
############################################################
#### 5. Some More Creative commands
############################################################

@bot.event
async def on_member_join(member):
    print("2nd branch called new member")
    channel = discord.utils.get(member.guild.text_channels, name="general")
    await channel.send(f"{member.name} has arrived!, Enjoy your stay at {member.guild.name}!")
    with open('images/welcome-neon.jpg', 'rb') as f:
        picture = discord.File(f)
        await channel.send(file=picture)

   
   
   
############################################################
#### 6. Actual Command
############################################################
#@bot.command()
#async def DM(ctx, user: discord.User, *, message=None):
#    message = "This Message is sent via DM"
#    await member.create_dm()
#    await member.dm_channel.send(
#        f'Hi {member.name}, welcome to my Discord server!')


############################################################
#### 7. Requests
############################################################
import requests
import json

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


############################################################
#### 8. Twitter
############################################################
import tweepy
import json
from pprint import pprint

api_key = os.getenv("api_key")
api_key_secret = os.getenv("api_key_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


user_name = 'BleepinComputer'

##### creates an array of tweets to post for today
tweets = api.user_timeline(screen_name=user_name, count=3)
print("tweets grabbed")


    

@bot.event
async def on_guild_join(guild):
    print("joined!")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            with open('images/Workshopassistant.jpeg', 'rb') as f:
                picture = discord.File(f)
                await channel.send(file=picture)
            await channel.send('**Hello World! I am Workshop Assistant** ')
            await channel.send("\"_Sometimes the smallest things make the biggest difference._\" ")
            await channel.send('- Greet New Members (!welcome)')
            await channel.send('- Fetch Tech-Related News (!news)')
            await channel.send('- Scheduler (Repeated Events)')
            await channel.send('- Remind you the Day and the Date (!clock)')
            await channel.send('- Send LoFi Vibes (!lofi)')

        break

    

############################################################
#### ... Run the Bot
############################################################
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
