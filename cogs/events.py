from string import Template

import discord
from discord.ext import commands

import config
from views.verify import VerifyCTA


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.welcome_template = Template(config.WELCOME_MESSAGE)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        context = {"GUILD_NAME": member.guild.name, "MENTION": member.mention}
        await member.send(
            self.welcome_template.safe_substitute(**context),
            view=VerifyCTA(),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Events(bot))
