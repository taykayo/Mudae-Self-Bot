import sys, traceback, configparser
import datetime as dt
from time import sleep
from scheduler.asyncio import Scheduler
from discord.ext import commands
from mudae import MudaeCommander
import threading

config = configparser.ConfigParser()
config.read('config.ini')
user_token = config['UserInfo']['token']
channel_id = int(config['ServerInfo']['channel_ID'])

prefix = "!"
mudae_channel = None
mudae = None
auto_roll_enabled = False
bot = commands.Bot(command_prefix="?", description="Weeb shit", request_guilds = False, self_bot=True)
cease_continuous_run = threading.Event()
threadyboi = None
schedule = None


#define checks
def is_me():
    def predicate(ctx):
        return ctx.message.author == bot.user
    return commands.check(predicate)

def is_mudae_channel():
    def predicate(ctx):
        return ctx.message.channel == mudae_channel
    return commands.check(predicate)

@bot.event
async def on_ready():
    global mudae_channel
    global mudae

    # Retrieve Mudae Channel, create mudae commander, and load commands
    mudae_channel = bot.get_channel(channel_id)
    mudae = MudaeCommander({},mudae_channel)
    cmds = await mudae_channel.application_commands()
    for cmd in cmds:
        if cmd.id == 832171928072224789:
            mudae.command_dict['tu'] = cmd
        if cmd.id ==832172151729422417:
            mudae.command_dict['wa'] = cmd
        if cmd.id ==832172457028747336:
            mudae.command_dict['ha'] = cmd
        if cmd.id ==832172216665374750:
            mudae.command_dict['wg'] = cmd
        if cmd.id ==832172416192872458:
            mudae.command_dict['hg'] = cmd
        if cmd.id ==832172261968314388:
            mudae.command_dict['wx'] = cmd
            mudae.command_dict['w'] = cmd
        if cmd.id ==832172373536669706:
            mudae.command_dict['hx'] = cmd
            mudae.command_dict['h'] = cmd
    print(f'Logged in as user {bot.user}')
    sleep(1)

@is_me()
@is_mudae_channel()
@bot.command(name='rollslam',
             aliases=['rs'])
async def roll_slam(ctx, category:str, rolls:int):
    if category in ['wa', 'wg', 'w', 'ha', 'hg', 'h']:
        if rolls > 0:
            print('Parsing successful')
            await mudae.send_rolls(category, rolls)
        else:
            await mudae_channel.send(f'Invalid number of rolls specified, must be > 0')
            return
    else:
        await mudae_channel.send(f'Invalid category specified. Valid categories are: wa, wg, w, ha, hg, h')
        return

@is_me()
@is_mudae_channel()
@bot.command(name='disableeautoroll',
             aliases=['dar'])
async def disable_auto_roll(ctx):
    global schedule
    schedule = Scheduler()
    await mudae_channel.send(f'Auto roll disabled')

@is_me()
@is_mudae_channel()
@bot.command(name='enableautoroll',
             aliases=['ear'])
async def enable_auto_roll(ctx, category:str, rolls:int, minute:int):
    global schedule
    schedule = Scheduler()
    schedule.hourly(dt.time(minute=minute, second=1), mudae.send_rolls, args=(category, rolls))
    # schedule.hourly(dt.time(minute=minute, second=1), mudae.send_timer)
    print(schedule)
    await mudae_channel.send(f'Auto roll enabled')

@is_me()
@is_mudae_channel()
@bot.command(name='checkar',
             aliases=['car'])
async def check_timers(ctx):
    await mudae_channel.send(f'{schedule}')


@is_me()
@is_mudae_channel()
@bot.command(name='checktimers',
             aliases=['ct'])
async def check_timers(ctx):
    await mudae.send_timer()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        pass
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
bot.run(user_token)


