import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions, has_role
from discord import Member
from discord import Embed,File
from typing import Optional
from random import choice
from asyncio import TimeoutError, sleep
from cogs.util import convert
import config as cfg

class Giveaway(commands.Cog):
    "Handles Giveaway related Commands"
    def __init__(self,bot):
        self.bot = bot
        self.cancelled = False

    @commands.hybrid_command(name="giveaway", aliases=["gift","gw", "gcreate", "gcr"])
    @has_permissions(manage_guild=True)
    async def create_giveaway(self, ctx):
        "Creates a giveaway"
        #Ask Questions
        embed = Embed(title="Giveaway Time!!✨",
                      description="Time for a new Giveaway. Answer the following questions in 25 seconds each for the Giveaway",
                      color=ctx.author.color)
        await ctx.send(embed=embed)
        questions=["In Which channel do you want to host the giveaway?",
                   "For How long should the Giveaway be hosted ? type number followed (s|m|h|d)",
                   "What is the Prize?"]
        answers = []
        #Check Author
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        for i, question in enumerate(questions):
            embed = Embed(title=f"Question {i}",
                          description=question)
            await ctx.send(embed=embed)
            try:
                message = await self.bot.wait_for('message', timeout=25, check=check)
            except TimeoutError:
                await ctx.send("You didn't answer the questions in Time")
                return
            answers.append(message.content)
        #Check if Channel Id is valid
        try:
            channel_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"The Channel provided was wrong. The channel should be {ctx.channel.mention}")
            return

        channel = self.bot.get_channel(channel_id)
        time = convert(answers[1])
        #Check if Time is valid
        if time == -1:
            await ctx.send("The Time format was wrong")
            return
        elif time == -2:
            await ctx.send("The Time was not conventional number")
            return
        prize = answers[2]

        await ctx.send(f"Your giveaway will be hosted in {channel.mention} and will last for {answers[1]}")
        embed = Embed(title="Giveaway Time !!",
                    description=f"Win a {prize} today",
                    colour=cfg.CLR)
        embed.add_field(name="Hosted By:", value=ctx.author.mention)
        embed.set_footer(text=f"Giveway ends in {answers[1]} from now")
        newMsg = await channel.send(embed=embed)
        await newMsg.add_reaction("🎉")
        #Check if Giveaway Cancelled
        self.cancelled = False
        await sleep(time)
        if not self.cancelled:
            myMsg = await channel.fetch_message(newMsg.id)

            users = await myMsg.reactions[0].users().flatten()
            users.pop(users.index(self.bot.user))
            #Check if User list is not empty
            if len(users) <= 0:
                emptyEmbed = Embed(title="Giveaway Time !!",
                                   description=f"Win a {prize} today")
                emptyEmbed.add_field(name="Hosted By:", value=ctx.author.mention)
                emptyEmbed.set_footer(text="No one won the Giveaway")
                await myMsg.edit(embed=emptyEmbed)
                return
            if len(users) > 0:
                winner = choice(users)
                winnerEmbed = Embed(title="Giveaway Time !!",
                                    description=f"Win a {prize} today",
                                    colour=cfg.CLR)
                winnerEmbed.add_field(name=f"Congratulations On Winning {prize}", value=winner.mention)
                winnerEmbed.set_image(url="https://firebasestorage.googleapis.com/v0/b/sociality-a732c.appspot.com/o/Loli.png?alt=media&token=ab5c8924-9a14-40a9-97b8-dba68b69195d")
                await myMsg.edit(embed=winnerEmbed)
                return

    # @create_giveaway.error
    # async def create_giveaway_error(self, ctx, exc):
    #     if isinstance(exc, MissingPermissions):
    #         await ctx.send("You are not allowed to create Giveaways")
        
    @commands.hybrid_command(name="giftrrl", aliases=["gifreroll", "gftroll", "grr"])
    @has_permissions(manage_guild=True)
    async def giveaway_reroll(self, ctx, channel: discord.TextChannel, id_: int):
        """
        Reroll a giveaway by picking a new winner from the users who reacted to the giveaway message.

        Args:
            ctx (commands.Context): The context of the command.
            channel (discord.TextChannel): The text channel where the giveaway message is located.
            id_ (int): The ID of the giveaway message to reroll.

        Raises:
            discord.Forbidden: If the bot doesn't have permission to manage the guild.
        """
        try:
            msg = await channel.fetch_message(id_)
        except:
            await ctx.send("The channel or ID mentioned was incorrect")
        
        users = await msg.reactions[0].users().flatten()
        
        if len(users) <= 0:
            emptyEmbed = Embed(title="Giveaway Time !!",
                            description=f"Win a Prize today")
            emptyEmbed.add_field(name="Hosted By:", value=ctx.author.mention)
            emptyEmbed.set_footer(text="No one won the Giveaway")
            await msg.edit(embed=emptyEmbed)
            return
        
        if len(users) > 0:
            winner = choice(users)
            winnerEmbed = Embed(title="Giveaway Time !!",
                                description=f"Win a Prize today",
                                colour=cfg.CLR)
            winnerEmbed.add_field(name=f"Congratulations On Winning Giveaway", value=winner.mention)
            winnerEmbed.set_image(url="https://firebasestorage.googleapis.com/v0/b/sociality-a732c.appspot.com/o/Loli.png?alt=media&token=ab5c8924-9a14-40a9-97b8-dba68b69195d")
            await msg.edit(embed=winnerEmbed)
            return


                # users.pop(users.index(self.bot.user))
                # winner = choice(users)
                # await channel.send(f"Congratulations {winner.mention} on winning the Giveaway")

    @commands.hybrid_command(name="giftdel", aliases=["gifdel", "gftdel", "gdl"])
    @has_permissions(manage_guild=True)
    # @has_role("admin")
    async def giveaway_stop(self, ctx, channel: discord.TextChannel, id_: int):
        """
        Stop and cancel a giveaway by updating its status and providing a cancellation message.

        Args:
            ctx (commands.Context): The context of the command.
            channel (discord.TextChannel): The text channel where the giveaway message is located.
            id_ (int): The ID of the giveaway message to cancel.

        Raises:
            discord.Forbidden: If the bot doesn't have permission to manage the guild.
        """
        try:
            msg = await channel.fetch_message(id_)
            newEmbed = Embed(title="Giveaway Cancelled", description="The giveaway has been cancelled!!")
            # Set Giveaway cancelled
            self.cancelled = True
            await msg.edit(embed=newEmbed)
        except:
            embed = Embed(title="Failure!", description="Cannot cancel Giveaway")
            await ctx.send(emebed=embed)

    @Cog.listener()
    async def on_ready(self):
        # await self.bot.stdout.send("Command Cog ready")
        if not self.bot.ready:
            self.bot.command_ready.ready_up("giveaway")

async def setup(bot):
    await bot.add_cog(Giveaway(bot))