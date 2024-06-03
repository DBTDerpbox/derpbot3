from cProfile import label
from pkgutil import extend_path
from pydactyl import PterodactylClient
import discord
from discord import app_commands
import random
import requests
import datetime
import pytz


#-! Config data !-#
token = open("data/configuration.txt", "r").readlines()[0].removeprefix("botsToken=").replace("\n", "") #-? Bot's token to login and run.
splashes = open("data/configuration.txt", "r").readlines()[3].removeprefix("splashesPath=").replace("\n", "") #-? Path to bot's random message on load.
lineNumber = random.randint (0, 436) #-? Change this number to how many lines there is in the splashes file.
discordURL = "https://discord.gg/cXtNz8XAua"
sourceURL = "https://github.com/DBTDerpbox/derpbot3"
mcAdminLogChannel = "derpbot-log"
mainGuild = 0 #Server ID replaces 0
appealGuild = 0 #Server ID replaces 0
pteroToken = "TokenforpterodactylHere"
pteroURL = "URLtopannel"
pteroMenuServer = "serverIDHere"
pteroBattle1Server = "serverIDHere"
pteroBattle4Server = "serverIDHere"
#-! Config data !-#

#Create a client to connect to the ptero panel and authenticate with the token
pteroAPI = PterodactylClient(pteroURL, pteroToken)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)


##Takes a code given by a user and checks if its correct
@tree.command(name = "verify", description="Enter the hidden phrase to verify yourself")
@app_commands.guilds(mainGuild)
@app_commands.describe(secret="The secret phrase")
async def verify(ctx: discord.Interaction, secret: str):
    role = 'Connecting to WFC...' #-? Role Name can be found in the roles menu. Grants the user the choosen role.
    verifyCode = 'toothpick' #-? when getting verified they need to use THIS code/term to verify with ?code [code/term].
    
    user = ctx.user #-? Gets user ID from who sent command

    if secret == verifyCode:
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))
        await ctx.response.send_message(content='You have successfully requested verification! Please be patient, as it may take some time for you to be verified.',ephemeral=True)
        channel = discord.utils.get(user.guild.channels, name="verification-list")
        await channel.send(f"User {user.mention} has successfully entered the code and is ready to be verified! <:fox:1028419395527135342>\nType `/accept <{user}>` to accept them!")
    else:
        await ctx.response.send_message(content='This phrase is incorrect! Please keep in mind it is case sensitive!',ephemeral=True)
        channel = discord.utils.get(user.guild.channels, name=mcAdminLogChannel)
        await channel.send(f"User {user.mention} has failed to type the code! Here's what they said: `"+secret+"`")


#Allow moderators to accept anyone who has typed the verification code correctly
@tree.command(name = "accept", description = "Verify a user")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(manage_roles=True)
@app_commands.describe(user="User to verify")
async def accept(ctx: discord.Interaction, user: discord.Member):

    oldRole = 'Connecting to WFC...' #-? Role Name can be found in the roles menu. Removes the choosen role from the user.
    role = 'Member' #-? Role Name can be found in the roles menu. Grants the user the choosen role.
    if discord.utils.get(user.guild.roles, name=role) in user.roles:
        await ctx.response.send_message("User <@"+str(user.id)+"> has already been verified!",ephemeral=True)
    else:
        #Send message
        try:
            await user.send("You have been verified in the [Legacy Edition Minigames] server! You now have access to channels, welcome to the community!")
            acceptNote = ""
        except:
            acceptNote = "\n**Note:** I do not have permission to dm this user! Their welcome message in dms will not be displayed on their end."
        await ctx.response.send_message(content="Verified user!"+acceptNote,ephemeral=True)
        #Set user roles
        await user.add_roles(discord.utils.get(user.guild.roles, name=role))
        await user.remove_roles(discord.utils.get(user.guild.roles, name=oldRole))
        channel = discord.utils.get(user.guild.channels, name="verification-list")
        await channel.send(f"User {user.mention} has been verified by "+str(ctx.user)+"! <a:xof:1038932012544827402>")


##Gets the player count of all lem servers and displays it
@tree.command(name = "status", description = "Display status of LEM Minecraft servers")
@app_commands.default_permissions(read_messages=True)
async def status(ctx):

    await ctx.response.send_message("Checking...")

    botPING = round(bot.latency * 1000)
    lem = requests.get(f"https://api.minetools.eu/ping/lem.derpbox.xyz").json()
    leb1 = requests.get(f"https://api.minetools.eu/ping/leb.derpbox.xyz").json()
    leb2 = requests.get(f"https://api.minetools.eu/ping/leb-2.derpbox.xyz").json()
    leb3 = requests.get(f"https://api.minetools.eu/ping/leb-3.derpbox.xyz").json()
    lebx = requests.get(f"https://api.minetools.eu/ping/test.leb.derpbox.xyz").json()
    lebg = requests.get(f"https://api.minetools.eu/ping/germany.leb.derpbox.xyz").json()
    
    #-! EMBED START !-#
    embed = discord.Embed(
        colour = discord.Color.from_rgb(5, 5, 5)
    )
    
    embed.add_field(name="Bot", value='```ini\n[{ping}ms]\n```'.format(ping=botPING))
    embed.set_author(name='Warning: Data may be inaccurate!')
    
    try:
        embed.add_field(name="Menu", value='```ini\n[{ping}ms]\n```\n```yaml\n[{players}/100 online]\n```'.format(ping=lem['latency'], players=lem['players']['online']))
    except:  
        embed.add_field(name="Menu", value='```css\n[offine(?)]\n```')
    
    try:
        embed.add_field(name="LEB - 1", value='```ini\n[{ping}ms]\n```\n```yaml\n[{players}/16 online]\n```'.format(ping=leb1['latency'], players=leb1['players']['online']))
    except:  
        embed.add_field(name="LEB - 1", value='```css\n[offine(?)]\n```')
        
    try:
        embed.add_field(name="LEB - 2", value='```ini\n[{ping}ms]\n```\n```yaml\n[{players}/16 online]\n```'.format(ping=leb2['latency'], players=leb2['players']['online']))
    except:  
        embed.add_field(name="LEB - 2", value='```css\n[offine(?)]\n```')
    
    try:
        embed.add_field(name="LEB - 3", value='```ini\n[{ping}ms]\n```\n```yaml\n[{players}/16 online]\n```'.format(ping=leb3['latency'], players=leb3['players']['online']))
    except:  
        embed.add_field(name="LEB - 3", value='```css\n[offine(?)]\n```')
        
    try:
        embed.add_field(name="LEB - Test", value='```ini\n[{ping}ms]\n```\n```yaml\n[{players}/16 online]\n```'.format(ping=lebx['latency'], players=lebx['players']['online']))
    except:  
        embed.add_field(name="LEB - Test", value='```css\n[offine(?)]\n```')

    try:
        embed.add_field(name="LEB - Germany", value='```ini\n[{ping}ms]\n```\n```yaml\n[{players}/16 online]\n```'.format(ping=lebg['latency'], players=lebg['players']['online']))
    except:  
        embed.add_field(name="LEB - Germany", value='```css\n[offine(?)]\n```')
    #-! EMBED END !-#

    await ctx.channel.send(embed=embed)


##Displays tutorial on how to use take everything
@tree.command(name = "takeall", description = "Show instructions on how to use Take Everything")
@app_commands.default_permissions(read_messages=True)
async def takeall(ctx):

    BridgeChatMessage = 'Vanilla: Double clicking on empty slots\n\nLEMClientHelper: Middle click'
    
    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.blue()
)
    DiscordChatMessage.add_field(name='How to take all in-game', value='```ini\nTake all is a feature in the [Battle Mini Game] used to take everything from a chest instantly.\n\nTo take everything in any version, you [Double click] in an [empty slot]. When using the [LEMClientHelper Mod] you can simply [Middle click].\n```', inline=False)
    #-! EMBED END !-#
    
    await ctx.response.send_message(embed=DiscordChatMessage)
    await ctx.channel.send(BridgeChatMessage, delete_after=0)


##Displays discord link
@tree.command(name = "discord", description = "Get discord link")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(read_messages=True)
async def discordcmd(ctx):
    
    await ctx.response.send_message(content=discordURL)
    await ctx.channel.send(content=discordURL, delete_after=0)


##Displays list of ips for lem servers
@tree.command(name = "ip", description = "Show list of IPs")
@app_commands.default_permissions(read_messages=True)
async def ip(ctx):
        
    BridgeChatMessage = 'Server IP: lem.derpbox.xyz'
    
    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.blue()
)
    DiscordChatMessage.add_field(name='Menu', value='```ini\n[lem.derpbox.xyz]\n```', inline=False)
    DiscordChatMessage.add_field(name='LEB - 1', value='```ini\n[leb.derpbox.xyz]\n```', inline=False)
    DiscordChatMessage.add_field(name='LEB - 2', value='```ini\n[leb-2.derpbox.xyz]\n```', inline=False)
    DiscordChatMessage.add_field(name='LEB - 3', value='```ini\n[leb-3.derpbox.xyz]\n```', inline=False)
    DiscordChatMessage.add_field(name='LEB - Experimental', value='```ini\n[test.leb.derpbox.xyz]\n```', inline=False)
    DiscordChatMessage.add_field(name='LEB - Germany', value='```ini\n[germany.leb.derpbox.xyz]\n```', inline=False)
    #-! EMBED END !-#
    
    await ctx.response.send_message(embed=DiscordChatMessage)
    await ctx.channel.send(BridgeChatMessage, delete_after=0)


##Displays some general information about derpbot3
@tree.command(name = "about", description = "Display general info about the bot")
@app_commands.default_permissions(read_messages=True)
async def about(ctx):

    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.blue(),
    title="Derpbot 3"
)
    DiscordChatMessage.add_field(name='About', value='Derpbot 3 is a discord bot made in Python for the Legacy Edition Minigames discord server.\n*To see available commands, run /help*', inline=False)
    DiscordChatMessage.add_field(name='Links', value='[Legacy Edition Minigames](http://lemsite.derpbox.xyz) | [Source Code]('+sourceURL+')', inline=False)
    #-! EMBED END !-#

    DiscordButtons = discord.ui.View()
    DiscordButtons.add_item(discord.ui.Button(label='LEM Website', style=discord.ButtonStyle.url, url="http://lemsite.derpbox.xyz"))
    DiscordButtons.add_item(discord.ui.Button(label='Source Code', style=discord.ButtonStyle.url, url=sourceURL))
    await ctx.response.send_message(embed=DiscordChatMessage,view=DiscordButtons)


##Displays all commands available to everyone
@tree.command(name = "help", description = "List available commands")
@app_commands.default_permissions(read_messages=True)
async def help(ctx):

    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.blue(),
    title="Command list"
)
    DiscordChatMessage.add_field(name='/about', value='See general info about Derpbot 3', inline=False)
    DiscordChatMessage.add_field(name='/help', value='List of available commands (you are here!)', inline=False)
    DiscordChatMessage.add_field(name='/discord', value='Get the current discord invite', inline=False)
    DiscordChatMessage.add_field(name='/takeall', value='Get help on how to use the Take Everything feature', inline=False)
    DiscordChatMessage.add_field(name='/status', value='Check all LEM servers for if they are online and get playercounts (if available)', inline=False)
    DiscordChatMessage.add_field(name='/ip', value='Show list of IP addresses to join LEM servers', inline=False)
    #-! EMBED END !-#

    await ctx.response.send_message(embed=DiscordChatMessage)


def isTempPunishment(duration, punishmentType):
    #Define global variables
    global punishmentDuration
    global punishmentCommand

    #Check if punishment duration is none or not
    if duration == "none":
        prefix = ""
        punishmentDuration = ""
    else:
        prefix = "temp"
        punishmentDuration = duration + " "
    punishmentCommand = prefix + punishmentType #Add the "temp" prefix to the original command if nessecary

def mcPunishment(punishmentType, commandSender, server, player, duration, reason):

    #Determine what server to use
    #Define global variables
    global punishmentMcServer
    global DiscordChatMessage
    global mcPunishmentNote
    
    #Find what server to use
    punishmentMcServer = pteroMenuServer #Default option
    targetServer = "Menu"
    if server == "1":
        punishmentMcServer = pteroBattle1Server
        targetServer = "Battle 1"
    if server == "experimental":
        punishmentMcServer = pteroBattle4Server
        targetServer = "Battle Experimental"

    #Run the command on the mc server
    isTempPunishment(duration, punishmentType) #Determine if is a temp punishment
    outputMcCommand = str.lower(punishmentCommand)+" "+player+" "+punishmentDuration+reason
    pteroAPI.client.servers.send_console_command(punishmentMcServer, outputMcCommand) #Send command to server
    print("Sending command to server "+targetServer+": "+outputMcCommand)

    #Prepare the discord message
    if punishmentMcServer == pteroMenuServer:
        mcPunishmentNote = "***NOTE: I do not recognize the server `"+server+"`, defaulting to Menu Server!***"
    else:
        mcPunishmentNote = ""
    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.red(),
    title="Punishment Info"
)
    DiscordChatMessage.add_field(name='Moderator', value=commandSender, inline=False)
    DiscordChatMessage.add_field(name='Player', value=player, inline=False)
    DiscordChatMessage.add_field(name='Punishment Type', value=punishmentType, inline=False)
    if duration == "none":
        DiscordChatMessage.add_field(name='Duration', value="Permanent", inline=False)
    else:
        DiscordChatMessage.add_field(name='Duration', value=duration, inline=False)
    DiscordChatMessage.add_field(name='Reason', value=reason, inline=False)
    DiscordChatMessage.add_field(name='Server', value=targetServer, inline=False)
    #-! EMBED END !-#


@tree.command(name = "mc-warn", description = "Warn a minecraft player")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(player="The username of the player to warn", server="The server to target (Menu by default)", reason="Reason to display as to why the player has been warned")
async def mcwarn(ctx: discord.Interaction, player: str, server: str, reason: str):

    #Do all the hard work
    mcPunishment("Warn", ctx.user, server, player, "7d", reason)

    #Send message in discord
    await ctx.response.send_message(content=mcPunishmentNote,embed=DiscordChatMessage,ephemeral=True)
    channel = discord.utils.get(ctx.user.guild.channels, name=mcAdminLogChannel)
    await channel.send(embed=DiscordChatMessage)


@tree.command(name = "mc-mute", description = "Mute a minecraft player")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(player="The username of the player to mute", server="The server to target (Menu by default)", duration="Length of mute (`none` for permanent)", reason="Reason to display as to why the player has been muted")
async def mcmute(ctx: discord.Interaction, player: str, server: str, duration: str, reason: str):

    #Do all the hard work
    mcPunishment("Mute", ctx.user, server, player, duration, reason)

    #Send message in discord
    await ctx.response.send_message(content=mcPunishmentNote,embed=DiscordChatMessage,ephemeral=True)
    channel = discord.utils.get(ctx.user.guild.channels, name=mcAdminLogChannel)
    await channel.send(embed=DiscordChatMessage)


@tree.command(name = "mc-unmute", description = "Unmute a minecraft player")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(player="The username of the player to unmute", server="The server to target (Menu by default)", reason="Reason to display as to why the player has been unmuted")
async def mcunmute(ctx: discord.Interaction, player: str, server: str, reason: str):

    #Do all the hard work
    mcPunishment("Unmute", ctx.user, server, player, "none", reason)

    #Send message in discord
    await ctx.response.send_message(content=mcPunishmentNote,embed=DiscordChatMessage,ephemeral=True)
    channel = discord.utils.get(ctx.user.guild.channels, name=mcAdminLogChannel)
    await channel.send(embed=DiscordChatMessage)


@tree.command(name = "mc-ban", description = "Ban a minecraft player")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(player="The username of the player to ban", server="The server to target (Menu by default)", duration="Length of ban (`none` for permanent)", reason="Reason to display as to why the player has been banned")
async def mcban(ctx: discord.Interaction, player: str, server: str, duration: str, reason: str):

    #Do all the hard work
    mcPunishment("Ban-IP", ctx.user, server, player, duration, reason)

    #Send message in discord
    await ctx.response.send_message(content=mcPunishmentNote,embed=DiscordChatMessage,ephemeral=True)
    channel = discord.utils.get(ctx.user.guild.channels, name=mcAdminLogChannel)
    await channel.send(embed=DiscordChatMessage)


@tree.command(name = "mc-unban", description = "Unban a minecraft player")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(ban_members=True)
@app_commands.describe(player="The username of the player to unban", server="The server to target (Menu by default)",  reason="Reason to display as to why the player has been unbanned")
async def mcban(ctx: discord.Interaction, player: str, server: str, reason: str):

    #Do all the hard work
    mcPunishment("Unban-IP", ctx.user, server, player, "none", reason)

    #Send message in discord
    await ctx.response.send_message(content=mcPunishmentNote,embed=DiscordChatMessage,ephemeral=True)
    channel = discord.utils.get(ctx.user.guild.channels, name=mcAdminLogChannel)
    await channel.send(embed=DiscordChatMessage)


@tree.command(name = "mc-kick", description = "Kick a minecraft player")
@app_commands.guilds(mainGuild)
@app_commands.default_permissions(kick_members=True)
@app_commands.describe(player="The username of the player to kick", server="The server to target (Menu by default)", reason="Reason to display as to why the player has been kicked")
async def mckick(ctx: discord.Interaction, player: str, server: str, reason: str):

    #Do all the hard work
    mcPunishment("Kick", ctx.user, server, player, "none", reason)

    #Send message in discord
    await ctx.response.send_message(content=mcPunishmentNote,embed=DiscordChatMessage,ephemeral=True)
    channel = discord.utils.get(ctx.user.guild.channels, name=mcAdminLogChannel)
    await channel.send(embed=DiscordChatMessage)


#Create the appeals menu and handle creating the channels for them
@tree.command(name = "appealmenu", description = "Display the menu to create an appeal")
@app_commands.guilds(appealGuild)
@app_commands.default_permissions(manage_messages=True)
async def appealmenu(ctx):

    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.blue(),
    title="Legacy Edition Minigames Appeals"
)
    DiscordChatMessage.add_field(name='About', value='If you have been banned or muted, you were likely linked to here.\nIf you believe your punishment is unfair, you are able to create an appeal with the button below.', inline=False)
    DiscordChatMessage.add_field(name='Note', value='**There is no guarantee you will be unbanned. Actions such as cheating are likely to not be appealed.**', inline=False)
    #-! EMBED END !-#

    #Prepare the appeal button
    appealButton = discord.ui.Button(label = "Create Appeal", style= discord.ButtonStyle.green)
    #Prepare the embed message to give when creating a new channel
    appealChatMessage = discord.Embed(
    colour = discord.Colour.blue(),
    title="Appeal Created")
    appealChatMessage.add_field(name='About', value='Your appeal has been created! Please tell us your **Username of banned account**, and **Why you think you should be unbanned.**', inline=False)
    appealChatMessage.add_field(name='Important Note', value='It could take a while for moderators to get to your appeal! Please be patient.', inline=False)
    #Create channel upon request
    async def appealButton_callback(interaction):
        role = 'Has created appeal' #-? Role Name can be found in the roles menu. Grants the user the choosen role.
        if discord.utils.get(interaction.user.guild.roles, name=role) in interaction.user.roles:
            await interaction.response.send_message("You have already created an appeal!",ephemeral=True)
        else:
            guild = interaction.message.guild
            category = discord.utils.get(interaction.guild.categories, name="Appeals")
            channel = await guild.create_text_channel(name="appeal-"+str(interaction.user).replace('#', '-'),reason="User requested to create appeal",category=category,topic="Created by <@"+str(interaction.user.id)+">\nCreated at "+str(datetime.datetime.now(pytz.timezone('America/Chicago'))))
            overwrites = channel.overwrites_for(interaction.user)
            overwrites.read_messages = True
            await channel.set_permissions(interaction.user, overwrite=overwrites)
            await interaction.response.send_message(f"Appeal created! please click here: <#"+str(channel.id)+">",ephemeral=True)
            await channel.send(embed=appealChatMessage,content="<@"+str(interaction.user.id)+"> <@&1041994886221676554>")
            #Give role for having an appeal open
            await interaction.user.add_roles(discord.utils.get(interaction.user.guild.roles, name=role))
    appealButton.callback = appealButton_callback

    #Add buttons
    DiscordButtons = discord.ui.View(timeout=None)
    DiscordButtons.add_item(item=appealButton)
    DiscordButtons.add_item(discord.ui.Button(label='See Rules', style=discord.ButtonStyle.url, url="http://lemsite.derpbox.xyz/rules"))

    await ctx.response.send_message(content="Opening the menu!",ephemeral=True)
    await ctx.channel.send(embed=DiscordChatMessage,view=DiscordButtons)

#Allow moderators to add anyone to an appeal
@tree.command(name = "add-user-to-appeal", description = "Add a user to an appeal")
@app_commands.guilds(appealGuild)
@app_commands.default_permissions(manage_channels=True)
@app_commands.describe(user="User to add to the appeal")
async def addusertoappeal(ctx: discord.Interaction, user: discord.Member):

    #Add user to channel
    overwrites = ctx.channel.overwrites_for(user)
    overwrites.read_messages = True
    await ctx.channel.set_permissions(user, overwrite=overwrites)
    #Send message
    await ctx.response.send_message(content="Added <@"+str(user.id)+"> to this appeal!")


#Allow moderators to remove anyone from an appeal
@tree.command(name = "remove-user-from-appeal", description = "Remove a user from an appeal")
@app_commands.guilds(appealGuild)
@app_commands.default_permissions(manage_channels=True)
@app_commands.describe(user="User to remove from the appeal")
async def removeuserfromappeal(ctx: discord.Interaction, user: discord.Member):

    #Add user to channel
    overwrites = ctx.channel.overwrites_for(user)
    overwrites.read_messages = False
    await ctx.channel.set_permissions(user, overwrite=overwrites)
    #Send message
    await ctx.response.send_message(content="Removed <@"+str(user.id)+"> from this appeal!")


#Allow moderators to close an appeal
@tree.command(name = "close-appeal", description = "Close an appeal")
@app_commands.guilds(appealGuild)
@app_commands.default_permissions(manage_channels=True)
async def closeappeal(ctx):

    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.red(),
    title="Closing the appeal"
)
    DiscordChatMessage.add_field(name='**Are you absolutely sure?**', value='Clicking `Yes, close this appeal` will disable the ability to chat in this channel and the ability to re-open the appeal will not exist. Only do this when you are ABSOLUTELY SURE you have done everything you need here!', inline=False)
    #-! EMBED END !-#

    #Prepare the appeal button
    closeButton = discord.ui.Button(label = "Yes, close this appeal", style= discord.ButtonStyle.red)
    #Prepare the embed message to give when closing the appeal
    closedChatMessage = discord.Embed(
    colour = discord.Colour.blue(),
    title="Appeal Closed")
    closedChatMessage.add_field(name='This appeal has been archived', value='The ability to chat in this appeal has been disabled, and the channel will exist here as an archive.', inline=False)
    closedChatMessage.add_field(name='Not done?', value='If you still need to continue the conversation you may create a new appeal in the create-appeal channel.', inline=False)
    #Close appeal upon request
    async def closeButton_callback(interaction):
        guild = interaction.message.guild
        #Remove role from user to created appeal
        channelTopic = interaction.channel.topic
        userID = channelTopic[channelTopic.find("@")+1 : channelTopic.find(">")] #Get the user's ID from the channel topic
        appealCreator = await guild.fetch_member(userID)
        await appealCreator.remove_roles(discord.utils.get(appealCreator.guild.roles, name="Has created appeal"))
        #Edit channel
        category = discord.utils.get(interaction.guild.categories, name="Appeals Archive")
        channel = await ctx.channel.edit(name="archived-appeal-"+str(appealCreator).replace('#', '-'),reason="Moderator "+str(interaction.user)+" requested to close appeal "+str(appealCreator),category=category)
        #Send messages
        await interaction.response.send_message(embed=closedChatMessage)
        #Disable the ability to chat and such
        overwrites = interaction.channel.overwrites_for(guild.default_role)
        overwrites.send_messages = False
        overwrites.send_messages_in_threads = False
        overwrites.add_reactions = False
        overwrites.use_application_commands = False
        await interaction.channel.set_permissions(guild.default_role, overwrite=overwrites)
        #Prevent anyone from messing with any messages
        moderatorRole = discord.utils.get(interaction.guild.roles, name="Moderator")
        overwrites = interaction.channel.overwrites_for(moderatorRole)
        overwrites.manage_messages = False
        overwrites.manage_channels = False
        await interaction.channel.set_permissions(moderatorRole, overwrite=overwrites)

    closeButton.callback = closeButton_callback

    #Add buttons
    DiscordButtons = discord.ui.View()
    DiscordButtons.add_item(item=closeButton)

    await ctx.response.send_message(embed=DiscordChatMessage,view=DiscordButtons,ephemeral=True)

@bot.event
async def on_message(ctx):
    if ctx.author == bot.user:
        return

    BridgeChatMessage = 'Vanilla: Double clicking on empty slots\n\nLEMClientHelper: Middle click'
    
    #-! EMBED START !-#
    DiscordChatMessage = discord.Embed(
    colour = discord.Colour.blue()
)
    DiscordChatMessage.add_field(name='How to take all in-game', value='```ini\nTake all is a feature in the [Battle Mini Game] used to take everything from a chest instantly.\n\nTo take everything in any version, you [Double click] in an [empty slot]. When using the [LEMClientHelper Mod] you can simply [Middle click].\n```', inline=False)
    #-! EMBED END !-#
    if ctx.content.startswith('?takeall'):
        await ctx.channel.send(embed=DiscordChatMessage)
        await ctx.channel.send(BridgeChatMessage, delete_after=0)
    
    if ctx.content.startswith('?discord'):
        await ctx.channel.send(discordURL)

    if "autoclick" in ctx.content.lower():
        await ctx.reply("The server has a CPS cap of 15, this can result in it looking like autoclicking if someone has a CPS above 15.")

    #Function for autobanning slurs
    def autoPunish(ctx, phrase, type, reason):
        ##Set global variables
        global mcUsername
        global channel
        global AutobanChatMessage
        ##Get channel to send log message in
        channel = discord.utils.get(ctx.guild.channels, name=mcAdminLogChannel)
        ##Get MC username
        mcUsername = str(ctx.author).replace('#0000', '')
        ##Create message for log channel
        #Blocked worlds
        if type == "blockedWords":
            AutobanChatMessage = "Player `"+mcUsername+"` said a banned phrase in chat and has been automatically banned! Phrase: ||"+phrase+"||\nFull message:||"+str(ctx.content)+"||"
        #Meteor ""Detection""
        if type == "meteor":
            AutobanChatMessage = "Player `"+mcUsername+"` said the meteor fancychat phrase in chat and has been automatically banned!\nFull message:||"+str(ctx.content)+"||"
        ##Get server the player is in
        server = str(ctx.channel).replace('battle-bridge-', '')
        ##Punish player
        #Blocked words
        if type == "blockedWords":
            mcPunishment("Mute", "Derpbot", server, mcUsername, "7d", reason)
            mcPunishment("Ban-IP", "Derpbot", server, mcUsername, "1m", reason)
        #Meteor ""detection""
        if type == "meteor":
            mcPunishment("Ban-IP", "Derpbot", server, mcUsername, "none", reason)
    
    #Autoban if slur is typed in chat by a minecraft user
    blockedWords = []
    for phrase in blockedWords:
        if phrase in ctx.content.lower():
            if ctx.author.bot:
                autoPunish(ctx, phrase, "blockedWords", "Slur usage is strictly prohibited on this server. §lIf you continue this behavior, there will be punishments.")
                await ctx.delete()
                await channel.send(AutobanChatMessage)

    #Autoban if the meteor fancychat phrase is said
    if "ᴍᴇᴛᴇᴏʀ ᴏɴ ᴄʀᴀᴄᴋ!" in ctx.content.lower():
        if ctx.author.bot:
            autoPunish(ctx, phrase, "meteor", "Cheating")
            await ctx.delete()
            await channel.send(AutobanChatMessage)


#-? Bot's status ?-#
with open(splashes, 'r', encoding='utf-8') as file:
        splash = file.readlines()[lineNumber] #-? Get random message.


@bot.event
async def on_ready():
    print(f"{splash}Logged in as {bot.user} running derpbot3!")
    await tree.sync()
    await tree.sync(guild=discord.Object(mainGuild))
    await tree.sync(guild=discord.Object(appealGuild))
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(splash))
#-? Bot's status.


bot.run(token) # run the bot with the token
