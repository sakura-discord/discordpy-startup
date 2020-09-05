from discord.ext import commands
import os
import traceback
import discord
import ast
import asyncio
import random
import datetime
import re
import aiohttp
import json
from discord.ext import commands,tasks

bot = commands.Bot(command_prefix='a)')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')
import discord
import ast
import asyncio
import random
import datetime
import re
import aiohttp
import json
from discord.ext import commands,tasks


@bot.command(name="eval")
@commands.is_owner()
async def eval_(ctx, *, cmd):
    def get_role(name):
        return discord.utils.get(ctx.guild.roles, name=name)

    def get_channel(name):
        return discord.utils.get(ctx.guild.channels, name=name)

    def get_member(name):
        return discord.utils.get(ctx.guild.members, name=name)

    try:
        fn_name = "_eval_expr"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        env = {
            'bot': ctx.bot,
            'discord': discord,
            'asyncio': asyncio, 'random': random, 'datetime': datetime,
            're': re, 'aiohttp': aiohttp, 'json': json,
            'commands': commands, 'tasks': tasks,
            'get_role': get_role, 'get_channel': get_channel, 'get_member': get_member,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        result = (await eval(f"{fn_name}()", env))
        await ctx.message.add_reaction("👍")
        if result is not None:
            if isinstance(result, discord.Embed):
                await ctx.send(embed=result)
            elif isinstance(result, discord.File):
                await ctx.send(file=result)
            elif isinstance(result, discord.Attachment):
                await ctx.send(file=await result.to_file())
            else:
                await ctx.send(result)
    except:
        embed = discord.Embed(color=0xFFFF00)
        embed.add_field(name="Error", value="```py\n{}```".format(traceback.format_exc()[:1024:]), inline=False)
        await ctx.send(embed=embed)
        await ctx.message.add_reaction("⚠️")
bot.run(token)
