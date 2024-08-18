import discord
from discord.ext import commands
import google.generativeai as genai
import os
import webserver

DISCORD_TOKEN = os.getenv('discordkey')
GEMINI_API_KEY = os.getenv('gemini_apikey')

genai.configure(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.command(name='ai')
async def ai(ctx, *, question: str = None):
    if not question:
        await ctx.send("Please provide a query.")
        return
    
    try:
        # Assuming genai.GenerativeModel is correct, replace if needed
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(question)
        
        if response and hasattr(response, 'text'):
            response_text = response.text
            for chunk in [response_text[i:i + 1900] for i in range(0, len(response_text), 1900)]:
                await ctx.send(chunk)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        # Consider logging the error as well for debugging
        print(f"Error: {e}")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
    webserver.keep_alive()  # Ensure this is implemented in your webserver module
