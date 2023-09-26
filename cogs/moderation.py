import config as cfg
import discord
from discord.ext import commands
import sqlite3

class Moderation(commands.Cog):
    "Mod Commands"
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('./db/warnings.db')
        self.cursor = self.conn.cursor()

    @commands.hybrid_command(name='warn')
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        """
        Warns a member and stores the warning in a database.

        Args:
            ctx (commands.Context): The context of the command.
            member (discord.Member): The member to be warned.
            reason (str, optional): The reason for the warning. Defaults to None.

        Raises:
            discord.Forbidden: If the bot lacks the required permissions.
        """
        if member == ctx.author:
            return await ctx.send("You can't warn yourself.")

        if reason is None:
            reason = "No reason provided."

        self.cursor.execute(f"INSERT INTO warnings VALUES ({member.id}, '{reason}')")
        self.conn.commit()

        embed = discord.Embed(title="Member Warned", description=f"{member.mention} was warned by {ctx.author.mention} for {reason}.", color=cfg.CLR)
        await ctx.send(embed=embed)

        try:
            await member.send(f"You were warned in {ctx.guild.name} for {reason}.")
        except discord.Forbidden:
            await ctx.send(f"{member.mention} was warned, but I couldn't DM them to tell them why.")

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Initializes the database table for warnings if it does not exist.
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS warnings (user_id INTEGER, reason TEXT)")
        self.conn.commit()

    @commands.hybrid_command(name='show_warnings')
    @commands.has_permissions(kick_members=True)
    async def warnshow(self, ctx, member: discord.Member):
        """
        Shows the warnings for a member.

        Args:
            ctx (commands.Context): The context of the command.
            member (discord.Member): The member to show warnings for.
        """
        self.cursor.execute(f"SELECT * FROM warnings WHERE user_id = {member.id}")
        warnings = self.cursor.fetchall()

        if not warnings:
            return await ctx.send(f"{member.mention} has no warnings.")

        embed = discord.Embed(title=f"{member.name}'s Warnings", color=cfg.CLR)
        for i, warning in enumerate(warnings):
            embed.add_field(name=f"Warning {i + 1}", value=warning[1], inline=False)

        await ctx.send(embed=embed)

    @commands.hybrid_command(name='removewarn')
    @commands.has_permissions(kick_members=True)
    async def removewarn(self, ctx, member: discord.Member, warning_number: int):
        """
        Removes a specific warning for a member.

        Args:
            ctx (commands.Context): The context of the command.
            member (discord.Member): The member from whom to remove the warning.
            warning_number (int): The number of the warning to remove.

        Raises:
            discord.Forbidden: If the bot lacks the required permissions.
        """
        self.cursor.execute(f"SELECT * FROM warnings WHERE user_id = {member.id}")
        warnings = self.cursor.fetchall()

        if warning_number > len(warnings):
            return await ctx.send(f"Warning {warning_number} does not exist for {member.mention}.")

        warning_to_remove = warnings[warning_number - 1]
        self.cursor.execute(f"DELETE FROM warnings WHERE user_id = {member.id} AND reason = '{warning_to_remove[1]}'")
        self.conn.commit()

        await ctx.send(f"Removed warning {warning_number} for {member.mention}.")
        
    @commands.hybrid_command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """
        Kicks a member from the server.

        Args:
            ctx (commands.Context): The context of the command.
            member (discord.Member): The member to kick.
            reason (str, optional): The reason for the kick. Defaults to None.

        Raises:
            discord.Forbidden: If the bot lacks the required permissions.
        """
        if member.id == ctx.author.id:
            return await ctx.send("You cannot kick yourself.")

        if member.id == self.bot.user.id:
            return await ctx.send("You cannot kick me.")

        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send("You cannot kick someone with a higher or equal role than you.")

        if member.top_role.position >= ctx.guild.me.top_role.position:
            return await ctx.send("You cannot kick someone with a higher or equal role than me.")

        try:
            await member.kick(reason=reason)
        except discord.Forbidden:
            return await ctx.send("I do not have permission to kick this member.")

        embed = discord.Embed(title="Member Kicked", color=cfg.CLR)
        embed.add_field(name="Member", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Kicked By", value=f"{ctx.author} ({ctx.author.id})", inline=False)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)

        await ctx.send(embed=embed)

        try:
            await member.send(f"You have been kicked from {ctx.guild.name} by {ctx.author}.\nReason: {reason if reason else 'No reason provided.'}")
        except discord.Forbidden:
            pass


    @commands.hybrid_command(name='ban')
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """
        Bans a member from the server.

        Args:
            ctx (commands.Context): The context of the command.
            member (discord.Member): The member to ban.
            reason (str, optional): The reason for the ban. Defaults to None.

        Raises:
            discord.Forbidden: If the bot lacks the required permissions.
        """
        if member.id == ctx.author.id:
            return await ctx.send("You cannot ban yourself.")

        if member.id == self.bot.user.id:
            return await ctx.send("You cannot ban me.")

        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send("You cannot ban someone with a higher or equal role than you.")

        if member.top_role.position >= ctx.guild.me.top_role.position:
            return await ctx.send("You cannot ban someone with a higher or equal role than me.")

        try:
            await member.ban(reason=reason)
        except discord.Forbidden:
            return await ctx.send("I do not have permission to ban this member.")

        embed = discord.Embed(title="Member Banned", color=cfg.CLR)
        embed.add_field(name="Member", value=f"{member} ({member.id})", inline=False)
        embed.add_field(name="Banned By", value=f"{ctx.author} ({ctx.author.id})", inline=False)
        if reason:
            embed.add_field(name="Reason", value=reason, inline=False)

        await ctx.send(embed=embed)

        try:
            await member.send(f"You have been banned from {ctx.guild.name} by {ctx.author}.\nReason: {reason if reason else 'No reason provided.'}")
        except discord.Forbidden:
            pass

async def setup(bot):
    await bot.add_cog(Moderation(bot))
        