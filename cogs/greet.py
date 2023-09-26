import discord
import config as cfg
import random
from discord.ext import commands

class Greeter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = cfg.GREETING
        greetings = [
    f"Welcome aboard, {member.mention}! 🎉 We're thrilled to have you join our server!",
    f"Hey there, {member.mention}! 😄 Thanks for joining our community. Welcome!",
    f"Hello and welcome, {member.mention}! 🌟 We hope you enjoy your time here!",
    f"Hi, {member.mention}! 🙌 So glad you decided to be a part of our server. Welcome!",
    f"Hey, {member.mention}! 🤗 We can't wait to get to know you better!",
    f"Hello new friend, {member.mention}! 🌈 Welcome to our wonderful server.",
    f"Hey, {member.mention}! 👋 Welcome to the party! Let's have some fun.",
    f"Greetings, {member.mention}! 🚀 It's a pleasure to have you here. Welcome!",
    f"Hi there, {member.mention}! 🌟 Your presence just made our day. Welcome!",
    f"Yo, {member.mention}! 🎈 We've been waiting for you. Welcome to the gang!"
]
        greet_msg = random.choice(greetings)
        await channel.send(greet_msg)

async def setup(bot):
    await bot.add_cog(Greeter(bot))

