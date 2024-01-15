import discord
from discord.ext import commands

class Embed(commands.Cog):
    """
    A Discord bot cog for creating and sending rich embeds.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
    """

    def __init__(self, bot):
        """
        Initializes the Embed cog.

        Args:
            bot (commands.Bot): The Discord bot instance.
        """
        self.bot = bot

    @commands.hybrid_command(name='embed')
    async def embed_(self, ctx: commands.Context, title: str = None, content: str = None, color: str = None, image: str = None, footer: str = None):
        """
        Creates and sends a rich embed message in the Discord channel.

        Args:
            ctx (commands.Context): The context of the command.
            title (str, optional): The title of the embed. Defaults to None.
            content (str, optional): The content/description of the embed. Defaults to None.
            color (str, optional): The color of the embed in hexadecimal format (e.g., "#RRGGBB"). Defaults to None.
            image (str, optional): The URL of an image to be displayed in the embed. Defaults to None.
            footer (str, optional): The footer text of the embed. Defaults to None.
        """
        embed = discord.Embed()
        if title:
            embed.title = title
        if content:
            embed.description = content
        if color:
            embed.color = discord.Color(color)  # Convert hexadecimal color to Discord Color
        if image:
            embed.set_image(url=image)
        if footer:
            embed.set_footer(text=footer)

        await ctx.send(embed=embed)

async def setup(bot):
    """
    A function to set up the Embed cog and add it to the bot.

    Args:
        bot (commands.Bot): The Discord bot instance.
    """
    await bot.add_cog(Embed(bot))
