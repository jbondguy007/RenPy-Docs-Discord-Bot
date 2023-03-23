import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import requests

bot = commands.Bot(command_prefix='r!', help_command=None, intents=discord.Intents.all())

load_dotenv()

TOKEN = os.getenv('TOKEN')
RENPY_SEARCH_API_KEY = os.getenv('RENPY_SEARCH_API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
googleapi_link = 'https://www.googleapis.com/customsearch/v1/siterestrict'
last_query = None
illegal_characters = '\/|:.?^*&%.#[]{}<>+="\'`„“_~'

def renpy_docs_query(query, index):

    if any(char in illegal_characters for string in query for char in string):
        return 'illegal_query'

    url = f"{googleapi_link}?key={RENPY_SEARCH_API_KEY}&cx={SEARCH_ENGINE_ID}&q={'+'.join(query)}"
    r = requests.get(url)
    results = r.json()
    
    if results['searchInformation']['totalResults'] == 0:
        return 'no_result'

    try:
        result = results['items'][index]
    except IndexError:
        result = None

    return result

@bot.event
async def on_ready():

    print("Logged in as {}".format(bot.user, bot.command_prefix))
    print("Ready!")
    await bot.change_presence(status=discord.Status.online)
    await bot.change_presence(activity=discord.Game(bot.command_prefix))

@bot.command()
async def docs(ctx, *query, index=0):

    # Setting global variables for the next() command to use
    global last_query
    global last_index
    last_query = query
    last_index = index

    result = renpy_docs_query(query, index)

    if result == 'no_result':
        await ctx.send("0 results found for this query.")
        return
    elif result == 'illegal_query':
        await ctx.send("Query includes illegal character. Alphanumerical characters are recommended.")
        return
    
    # For the next() command - If there are no more results at this index position
    if not result:
        await ctx.send(f"Reached end of results for last query! Issue a `{bot.command_prefix}docs <query>` command first.")
        return

    title = result['title']
    link = result['link']
    snippet = result['snippet']

    embed = discord.Embed(title=title, description=link)
    embed.add_field(name='', value=snippet)
    embed.set_footer(text=f'Result #{index+1}')

    await ctx.send(embed=embed)

@bot.command()
async def next(ctx):

    if last_query:
        command = bot.get_command('docs')
        await ctx.invoke(command, *last_query, index=last_index+1)

    else:
        await ctx.send(f"Issue a `{bot.command_prefix}docs <query>` command first!")

bot.run(TOKEN)