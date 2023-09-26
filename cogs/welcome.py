import discord
from discord.ext import commands
from discord.ui import View, Button
import config as cfg


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed=discord.Embed(color=cfg.CLR, title="ㅤ*:Butterfly: 𓂃 Welcome 𓂃 :Butterfly:**")
        button1 = Button(label='Rules', url="https://discord.com/channels/1155450070787960974/1155450463337066546",
                       emoji='<:rules:1064514958278266931>')

        button2 = Button(label='Roles',
                       url="https://discord.com/channels/1155450070787960974/1155450465950113794",
                       emoji='<:gc:1150762439789527100>')

        button3 = Button(label='Events',
                       url="https://discord.com/channels/1155450070787960974/1155450470555459584",
                       emoji='<:store:1064877285859147817>')

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        embed.description = f"""
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧
Stay with us !

!﹒♡𓂃ᵔᴗᵔ i hope you enjoy here 
!﹒♡𓂃ᵔᴗᵔ Now we have {member.guild.member_count} !! 
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧
"""
        embed.set_image(url="https://media.discordapp.net/attachments/1150321238997205002/1150359106008395846/welcome.png?width=1025&height=202")
        embed.set_footer(text=f'{member.guild.name} | {member.guild.id}', icon_url=member.guild.icon.url)
        channel = member.guild.get_channel(cfg.WELCOME)
        await channel.send(content=member.mention,embed=embed, view=view)
        await member.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Welcome(bot))