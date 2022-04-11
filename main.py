import discord
import os
import requests
import json
import random
from replit import db
from discord.ext import commands


client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "miserable", "hopeless"]
starter_encouragements = ["Cheer up!", "Hang in there", "You are amazing"]
banned_words = ["fuck", "bitch", "shit"]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragement(encouraging_message):
  if "encouragments" in db.keys():
   encouragements = db["encouragements"]
   encouragements.append(encouraging_message)
   db["encouragements"] = encouragements
  else: 
   db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('We have logged in as {0.user}' .format(client))
  
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content  
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  options = starter_encouragements
  if "encouragments" in db.keys():
    options = options + db["encouragements"]

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ", 1)[1]
    update_encouragement(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$ban"):
    async def ban(ctx, member : discord.Member, *, reason = None):
      await member.ban(reason = reason)

  if msg.startswith("$kick"):
    async def kick(ctx, member : discord.Member, *, reason = None):
      await member.ban(reason = reason)
  for words in banned_words:
    if words in msg.lower():
        await message.channel.send("Please do not use inappropriate language.")
     
client.run(os.getenv('TOKEN'))



