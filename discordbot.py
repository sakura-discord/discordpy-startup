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
#prefix定義,help無効化
bot = commands.Bot(command_prefix=["a)"], help_command=None)
token = os.environ['DISCORD_BOT_TOKEN']

#ERRORのなんか
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)
#testcommand
@bot.command()
async def test(ctx):
    await ctx.send('OK')
#開発環境が迷子になった時用
@bot.command()
async def code(ctx):
    await ctx.send('コードはこちらですを: https://github.com/null1981/discordpy-startup')

@bot.command()
async def help(ctx):
    await ctx.send('```‌prefix=a)\n\nhelp\n  :command一覧(これ)\ncode\n  :githubを出す\ntest\n  :OKと帰ってくるだけです\ndm*\n  :dmを送りつける\neval*\n  :実験用コマンド\nNote:*は権限が必要```')
#eval
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
#dmを送りつける
@bot.command()
@commands.is_owner()
async def dm(ctx, user : discord.User, *, message):
    await user.send(message)
    await ctx.message.add_reaction("✅")
#play
@bot.event
async def on_ready():
    activity = discord.Game(name="夜の運動会", type=3)
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=activity)
    print("ぎばらは元気に動いてます")
              

bot.run(token)
