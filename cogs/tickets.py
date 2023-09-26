import time
import discord
from discord.ext import commands

import config as cfg


class TICKET(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Ticket', style=discord.ButtonStyle.green, custom_id='Ticket:green')
    async def ticketopen(self, interaction=discord.Interaction, button=discord.ui.Button):
        category = discord.utils.get(interaction.guild.categories, id=int(cfg.TICKET))
        ticket = await category.create_text_channel(name=f'ticket-{interaction.user.name}')
        support = discord.utils.get(interaction.guild.roles, id=int(cfg.SUPPORT))
        overwrites = {
            support: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True,
                manage_messages=True,
                manage_permissions=True
            ),
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False,
                view_channel=False
            ),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
            )}
        await ticket.edit(overwrites=overwrites)

        await interaction.response.send_message(f'Your Ticket has been opened. Please move to {ticket.mention}',
                                                ephemeral=True)
        # await ticket.send(f'{interaction.user.mention} Help will be with you shortly.')
        embed = discord.Embed(title=f'{interaction.user.name}',
                              description=f'This ticket is opened by {interaction.user.mention}.',
                              color=cfg.CLR)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'{interaction.guild.name} | {interaction.guild.id}', icon_url=interaction.guild.icon.url)
        view = CLOSE()
        msg = await ticket.send(content=f'{interaction.user.mention} | <@&{int(cfg.SUPPORT)}>', embed=embed, view=view)
        await msg.pin()


class Ticket(commands.Cog):
    """This is responsible for the ticket system"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(TICKET())
        self.bot.add_view(CLOSE())

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def TICK(self, ctx):
        embed = discord.Embed(title='TICKET', description=f'PRESS THE BUTTON TO OPEN A TICKET',
                              color=cfg.CLR)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'{ctx.guild.name} | {ctx.guild.id}', icon_url=ctx.guild.icon.url)
        view = TICKET()
        await ctx.send(embed=embed, view=view)


class CLOSE(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='CLOSE', style=discord.ButtonStyle.danger, custom_id='CLOSE:RED')
    async def closeticket(self, interaction=discord.Interaction, button=discord.ui.Button, ):
        await interaction.channel.send(f'This ticket was closed by {interaction.user.mention}')
        channel = interaction.channel
        time.sleep(10)
        await channel.delete()


async def setup(bot):
    await bot.add_cog(Ticket(bot))
