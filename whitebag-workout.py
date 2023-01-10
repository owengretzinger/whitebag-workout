import random
import discord
import asyncio
from discord.ext import commands

client = commands.Bot(command_prefix = '!')
client.remove_command('help')


global server_members, guildID, data
server_members = []
guildID = -1

#data already in file
try:
    with open("Pushups.txt", "r") as f:
        data = []
        for line in f:
            data.append(line.partition('\n')[0])
except Exception as e:
    print(e)


@client.event
async def on_ready():
    global server_members, data, guildID
    print('bot is ready')



    #adding whatever isn't already in file
    server_members = client.get_guild(guildID).members
    workout_role = discord.utils.get(client.get_guild(guildID).roles, name = 'whitebag workout')

    for j in range(0, len(server_members)):

        names = get_name_list()

        if workout_role in server_members[j].roles and server_members[j].display_name not in names:
            data.append(server_members[j].display_name + ';0;0')

    data.sort(key=lambda x: x.lower())



#update the data in the file every 5 seconds
async def update_stats():
    global server_members, data
    await client.wait_until_ready()

    while not client.is_closed():
        try:
            with open("Pushups.txt", "w") as g:
                g.write('\n'.join(data))
                """
                if len(server_members) > 0:
                    data = []
                    for j in range(0, len(buff_guys)):
                        #print(str)
                        data.append(buff_guys[j] + ';' + str(pushups[j]))

                    print(data)

                    
                """
            await asyncio.sleep(5)
        except Exception as e:
            print(e)
            await asyncio.sleep(5)



#adding push ups for everyone when someone gets a white bag
@client.command()
async def add(ctx, *, amountString="z"):
    global data
    if amountString.isdigit():

        amount = int(amountString)
        name_list = get_name_list()
        pushup_list = get_pushup_list()
        leader_board_list = get_leader_board_list()

        member_index = name_list.index(ctx.author.display_name)



        for i in range(0, len(data)):
            if i != member_index:
                pushup_list[i] += amount
            else:
                pushup_list[i] += amount * 2
                leader_board_list[i] += amount
            data[i] = data[i].partition(';')[0] + ';' + str(pushup_list[i]) + ';' + str(leader_board_list[i])

        await ctx.send(f'Added {amount * 2} push ups for you, and {amount} for everyone else! Everyone say thank you {ctx.author.display_name}!')
    else:
        await ctx.send('Invalid amount.')



# in case someone messes up and needs to undo it
@client.command()
async def undo(ctx, *, amountString="z"):
    global data
    if amountString.isdigit():

        amount = int(amountString)
        name_list = get_name_list()
        pushup_list = get_pushup_list()
        leader_board_list = get_leader_board_list()

        member_index = name_list.index(ctx.author.display_name)
        leader_board_list[member_index] -= amount

        for i in range(0, len(data)):
            pushup_list[i] -= amount
            data[i] = data[i].partition(';')[0] + ';' + str(pushup_list[i]) + ';' + str(leader_board_list[i])

        await ctx.send(f'Wow, whoever messed up is dumb! Removed {amount} push ups for everyone, but whoever messed up will have to do some extra.')
    else:
        await ctx.send('Invalid amount.')



# removes push ups for specific person (to use after doing a set)
@client.command()
async def did(ctx, *, amountString="z"):
    global data
    if amountString.isdigit():

        amount = int(amountString)
        name_list = get_name_list()
        pushup_list = get_pushup_list()
        leader_board_list = get_leader_board_list()

        member_index = name_list.index(ctx.author.display_name)

        pushup_list[member_index] -= amount

        data[member_index] = data[member_index].partition(';')[0] + ';' + str(pushup_list[member_index]) + ';' + str(leader_board_list[member_index])

        await ctx.send(f'Big man! You have {pushup_list[member_index]} push ups remaining.')
    else:
        await ctx.send('Invalid amount.')



# short for remaining: shows how many push ups the person who sent the command has left to do
@client.command()
async def r(ctx):
    global data
    name_list = get_name_list()
    pushup_list = get_pushup_list()

    member_index = name_list.index(ctx.author.display_name)

    await ctx.send(f'{ctx.author.display_name} has {pushup_list[member_index]} push ups remaining.')



# shows how many push ups everyone has left to do
@client.command()
async def everyone(ctx):
    global data
    message = ""
    name_list = get_name_list()
    pushup_list = get_pushup_list()

    for j in range(0, len(data)):
        message += f'{name_list[j]} has {pushup_list[j]} push ups remaining.\n'

    await ctx.send(message)



# in case for some reason someone needs to override their push up number
@client.command()
async def override(ctx, *, amountString="z"):
    global data
    if amountString.isdigit():

        amount = int(amountString)
        name_list = get_name_list()
        pushup_list = get_pushup_list()
        leader_board_list = get_leader_board_list()

        member_index = name_list.index(ctx.author.display_name)

        pushup_list[member_index] = amount
        data[member_index] = data[member_index].partition(';')[0] + ';' + str(pushup_list[member_index]) + ';' + str(leader_board_list[member_index])

        await ctx.send(f'Hmmm... I suspect cheating... You have now have {pushup_list[member_index]} push ups remaining.')
    else:
        await ctx.send('Invalid amount.')



# shows a leaderboard of how much push ups each person has made everyone do
@client.command()
async def leaderboard(ctx):
    global data
    message = ""
    #name_list = get_name_list()
    #leader_board_list = get_leader_board_list()






    x = get_leader_board_list()
    y = get_name_list()
    leader_board_list = []
    name_list = []

    lowest = x[0]
    while len(x) > 0:
        place = 0
        for i in range(0, len(x)):
            if x[i] <= lowest:
                place = i
                lowest = x[i]
        leader_board_list.append(x[place])
        name_list.append(y[place])
        x.pop(place)
        y.pop(place)
        if len(x) > 0:
            lowest = x[0]

    leader_board_list.reverse()
    name_list.reverse()


    print(leader_board_list)

    for j in range(0, len(data)):
        message += f'{j + 1}. {name_list[j]}: {leader_board_list[j]} points\n'

    await ctx.send(message)



# shows personal total (leaderboard total + personal points - push ups remaining)
@client.command()
async def total(ctx):
    global data
    name_list = get_name_list()
    pushup_list = get_pushup_list()
    leaderboard_list = get_leader_board_list()

    member_index = name_list.index(ctx.author.display_name)

    total_pushups = 0
    for i in range(0, len(leaderboard_list)):
        total_pushups += leaderboard_list[i]

    total_pushups += leaderboard_list[member_index]
    total_pushups -= pushup_list[member_index]


    await ctx.send(f'You have done {total_pushups} push ups since I joined the server!')



# same as total but shows everyone
@client.command()
async def guildtotal(ctx):
    global data
    message = "Since adding me to the server:"

    for i in range(0, len(data)):
        name_list = get_name_list()
        pushup_list = get_pushup_list()
        leaderboard_list = get_leader_board_list()

        total_pushups = 0
        for j in range(0, len(leaderboard_list)):
            total_pushups += leaderboard_list[j]

        total_pushups += leaderboard_list[i]
        total_pushups -= pushup_list[i]

        message += f'\n{name_list[i]} has done {total_pushups} push ups.'

    await ctx.send(message)




# removes or adds the role, adds/removes them to data array
@client.command()
async def role(member):
    global data

    workout_role = discord.utils.get(client.get_guild(guildID).roles, name = 'whitebag workout')

    # if they already have the role, remove it
    if workout_role in member.author.roles:

        name_list = get_name_list()

        member_index = name_list.index(member.author.display_name)

        data.pop(member_index)

        await member.author.remove_roles(workout_role)
        await member.send(f'Oh, so you think you\'re already buff enough. I see how it is. Removed {workout_role} role.')

    # if they don't have the role, add it
    else:

        data.append(member.author.display_name + ';0;0')

        data.sort(key=lambda x: x.lower())

        await member.author.add_roles(workout_role)
        await member.send(f'Welcome to the club! Added {workout_role} role.')



# if someone with the role leaves the server, remove them
@client.event
async def on_member_remove(member):
    print('member left!')
    global data
    workout_role = discord.utils.get(client.get_guild(guildID).roles, name='whitebag workout')

    if workout_role in member.roles:

        name_list = get_name_list()

        member_index = name_list.index(member.display_name)

        data.pop(member_index)



# shows what every command does
@client.command()
async def help(ctx):

    desc = '**!add [amount]**\nadds specified amount of pushups for EVERYONE, and double the amount for you.\n'
    desc += '\n**!did [amount]**\nsubtract specified amount of pushups from your total (only typing "!did" will default to remove 5).\n'
    desc += '\n**!r**\nshows how many pushups you have left to do. (short for remaining)\n'
    desc += '\n**!role**\ngives you the whitebag workout role (or removes it).\n'
    desc += '\n**!everyone**\nshows how many pushups everyone has to do.\n'
    desc += '\n**!leaderboard**\nshows a leaderboard of how many push ups everyone has made each other do (NOT how many push ups each person has done).\n'
    desc += '\n**!undo [amount]**\nremoves [amount] from everyone, for when you mess up, although it won\'t remove double for you & so you will have to do extra for messing up.\n'
    desc += '\n**!override [amount]**\nsets your pushups left to do to amount (do not use).\n'
    desc += '\n**!total**\nshows how many push ups you\'ve done since May 27, 2020.\n'
    desc += '\n**!guildtotal**\nshows how many push ups EVERYONE has done since May 27, 2020.\n'
    desc += '\n**!top**\nshows the bags that added the most push ups to everyone since May 27, 2020.\n'

    embed = discord.Embed(colour=discord.Colour.from_rgb(250, 250, 250), timestamp=ctx.message.created_at, description=desc)

    embed.set_author(name='Help', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed)



# partitions the data to return only a list of names
def get_name_list():
    global data
    names = []
    for j in range(0, len(data)):
        names.append(data[j].partition(';')[0])
    return names

# partitions the data to return only a list of push ups as integers
def get_pushup_list():
    global data
    pushup_list = []
    for j in range(0, len(data)):
        pushup_list.append(int(data[j].partition(';')[2].partition(';')[0]))
    return pushup_list

# partitions the data to return only a list of push ups as integers
def get_leader_board_list():
    global data
    leader_board_list = []
    for j in range(0, len(data)):
        leader_board_list.append(int(data[j].partition(';')[2].partition(';')[2]))

    return leader_board_list



# easter eggs
@client.command()
async def oryx(ctx):

    await ctx.send('NOOOOO! THIS CANNOT BE! Hehe, I\'ve been practicing that one...')

@client.command()
async def pots(ctx):
    await ctx.send('Need to refill your potions?\nHere!')
    await ctx.send('https://i.imgur.com/DfYClhz.png https://i.imgur.com/t9LfFtV.png')
    await ctx.send('That should last like 0.2 seconds.')



client.loop.create_task(update_stats())
client.run('token')
