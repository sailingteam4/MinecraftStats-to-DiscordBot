import discord
import mcstats
from dotenv import load_dotenv
import os

load_dotenv()
bot = discord.Bot()
sftp = mcstats.coserv(os.getenv('HOST'), os.getenv('USER'), os.getenv('PASS'), os.getenv('PORT'))

def maintainco():
    global sftp
    if sftp.get_channel() is None:
        sftp.close()
        sftp = mcstats.coserv(os.getenv('HOST'), os.getenv('USER'), os.getenv('PASS'), os.getenv('PORT'))

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "time", description = "Get a player's playing time!")
@discord.option("pseudo", description="Minecraft username", required=True)
async def time(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        time = mcstats.gettime(stats)
        await ctx.respond(f"`{pseudo} played for {str(time)} hours on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")

@bot.slash_command(name = "jump", description = "Get the number of jump of a player")
@discord.option("pseudo", description="Minecraft username", required=True)
async def jump(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        jump = mcstats.getjump(stats)
        await ctx.respond(f"`{pseudo} jumped {str(jump)} times on th server`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
    
@bot.slash_command(name = "bell", description = "Get the number of bells rung by a player")
@discord.option("pseudo", description="Minecraft username", required=True)
async def bell(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        cloche = mcstats.getcloche(stats)
        await ctx.respond(f"`{pseudo} rung {str(cloche)} bells on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
    
@bot.slash_command(name = "mined", description = "Get the number of mined blocs of a player")
@discord.option("pseudo", description="Minecraft username", required=True)
async def mined(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        miner = mcstats.getminer(stats)[0]
        await ctx.respond(f"`{pseudo} mined {str(miner)} blocs on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
    
@bot.slash_command(name = "dead", description = "Get a player's death number")
@discord.option("pseudo", description="Minecraft username", required=True)
async def dead(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        mort = mcstats.getmort(stats)[0]
        await ctx.respond(f"`{pseudo} died {str(mort)} times on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
    
@bot.slash_command(name = "distance", description = "Get the distance reached by a player in kilometers")
@discord.option("pseudo", description="Minecraft username", required=True)
async def distance(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        dist = mcstats.getdistance(stats)
        await ctx.respond(f"`{pseudo} traveled {str(dist)} kilometers on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
      
@bot.slash_command(name="broke", description="Get the number of tools broke by a player")
@discord.option("pseudo", description="Minecraft username", required=True)
async def broke(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        brokes = mcstats.getbroke(stats)
        await ctx.respond(f"`{pseudo} broke{str(brokes)} tools on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
    
@bot.slash_command(name="killed", description="Get the number of monster killed by a player")
@discord.option("pseudo", description="Minecraft username", required=True)
async def killed(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        killed = mcstats.getkilled(stats)[0]
        await ctx.respond(f"`{pseudo} killed {str(killed)} monsters on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
    
@bot.slash_command(name = "crafted", description = "Get the number of items crafted by a player")
@discord.option("pseudo", description="Minecraft username", required=True)
async def crafted(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        crafted = mcstats.getcrafted()[0]
        await ctx.respond(f"`{pseudo} crafted {crafted} items on the server !`")
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")

@bot.slash_command(name = "card", description = "Get a statistics card for a player")
@discord.option("pseudo", description="Minecraft username", required=True)
async def card(ctx, pseudo):
    await ctx.defer()
    maintainco()
    stats = mcstats.getstat(sftp, pseudo)
    if stats:
        card = mcstats.getstats(stats)
        embed=discord.Embed(title=f"Statistics of {pseudo}", color=0x001eff)
        embed.set_thumbnail(url=f"https://mc-heads.net/head/{pseudo}/left")
        embed.add_field(name=str(card["time_played"]), value="Hours spent", inline=True)
        embed.add_field(name=str(card["jumps"]), value="Jumps", inline=True)
        embed.add_field(name=str(card["distance_travelled"]), value="Kilometers traveled", inline=True)
        embed.add_field(name=str(card["total_killed"]), value="Mob killed", inline=True)
        embed.add_field(name=str(card["cloche_ring"]), value="Bells rung", inline=True)
        embed.add_field(name=str(card["total_mined"]), value="Mined blocs", inline=True)
        embed.add_field(name=str(card["total_crafted"]), value="Crafted blocs (craft/furnace/anvil...)", inline=True)
        embed.add_field(name=str(card["total_deaths"]), value="Death", inline=True)
        embed.add_field(name=str(card["total_broken"]), value="Broke tools", inline=True)
        if "most_mined" in card.keys():
            embed.add_field(name=card["most_mined"].replace("minecraft:","").capitalize(), value=f"This is your most mined bloc ! It represents {str(card['most_mined_percent'])}% of all the blocs you mined", inline=False)
        if "most_killed" in card.keys():
            embed.add_field(name=card["most_killed"].replace("minecraft:","").capitalize(), value=f"This is your most killed monsters ! It represents {str(card['most_killed_percent'])}% of all the monsters you killed", inline=False)
        if "most_crafted" in card.keys():
            embed.add_field(name=card["most_crafted"].replace("minecraft:","").capitalize(), value=f"This is your most crafted items! It represents {str(card['most_crafted_percent'])}% of all the items you crafted", inline=False)
        if "most_death" in card.keys():
            embed.add_field(name=card["most_death"].replace("minecraft:","").capitalize(), value=f"It is your most dangerous enemy ! It represents {str(card['most_death_percent'])}% of all your death", inline=False)
        await ctx.respond(embed=embed)
        
    else:
        await ctx.respond(f"`{pseudo} never logged on the server`")
    
@bot.slash_command(name = "timeld", description = "Display the players time leaderboard")
async def timeld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.gettimeld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Time leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" hours", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
    
@bot.slash_command(name = "jumpld", description = "Display the players jump leaderboard")
async def jumpld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getjumpld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Jump leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" jumps", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
        
@bot.slash_command(name = "bellld", description = "Display the players bell leaderboard")
async def bellld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getclocheld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Bell leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" bells rung", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
        
@bot.slash_command(name = "brokenld", description = "Display the players broken tools leaderboard")
async def brokenld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getbrokeld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Broken tools leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" tools broke", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
        
@bot.slash_command(name = "distanceld", description = "Display the players distance leaderboard")
async def distanceld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getdistanceld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Distance leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" km", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
        
@bot.slash_command(name = "minedld", description = "Display the players mined blocs leaderboard")
async def minedld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getminerld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Mined blocs leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" mined blocs", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
        
@bot.slash_command(name = "deadld", description = "Display the players death leaderboard")
async def deadld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getmortld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Death leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" death", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
        
@bot.slash_command(name = "killedld", description = "Display the players monsters killed leaderboard")
async def killedld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getkilledld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Monsters killed leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" monsters killed", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
    
@bot.slash_command(name = "craftedld", description = "Display the players items crafted leaderboard")
async def craftedld(ctx):
    await ctx.defer()
    maintainco()
    stats = mcstats.getcraftedld(mcstats.getallstats(mcstats.lstfiles(sftp), sftp))
    if stats:
        emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
        e=discord.Embed(title="Crafted items leaderboard", color=0x001eff)
        for j in range(len(stats[:10])):
            e.add_field(name=emoji[j]+" "+stats[j][0], value=str(stats[j][1])+" items crafted", inline=False)
        await ctx.respond(embed=e)
    else:
        await ctx.respond("`Failed to retrieve statistics`")
        
bot.run(os.getenv('TOKEN'))