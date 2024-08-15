import discord
from discord.ext import commands
import google.generativeai as genai
import os
import webserver


DISCORD_TOKEN = os.environ['discordkey']
GEMINI_API_KEY = 'AIzaSyBwbrA4iMHR-TiEe_IWm2PEV5U-5Yn2Ok8'

genai.configure(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.command(name='ai')
async def ai(ctx, *, question):
    if not question:
        await ctx.send("Please provide a Query")
        return
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        if response and hasattr(response, 'text'):
            response_text = response.text
            for chuck in [response_text[i:i + 1900] for i in range(0,len(response_text), 1900)]:
                await ctx.send(chuck)

    except Exception as e:
        await ctx.send(f"an error as occured: {e}")

bot.run(DISCORD_TOKEN)        
webserver.keep_alive()