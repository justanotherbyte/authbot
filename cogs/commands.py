from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

import config

if TYPE_CHECKING:
    from bot import AuthBot


class CommandsCog(commands.Cog):
    @app_commands.command(
        description="Verify yourself to access restricted channels of this and other guilds."
    )
    @app_commands.guild_install()
    @app_commands.guild_only()
    async def verify(self, interaction: discord.Interaction["AuthBot"]):
        await interaction.response.defer(ephemeral=True, thinking=True)

        async with interaction.client.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT authenticated_at FROM authenticated_users WHERE user_id = $1",
                interaction.user.id,
            )

        if row is None:
            return await interaction.followup.send(
                "You aren't authenticated. Please either re-join or run the `/invokeauth` command."
            )

        assert interaction.guild is not None
        role = interaction.guild.get_role(config.AUTHENTICATED_ROLE_ID)

        assert isinstance(interaction.user, discord.Member)
        if role in interaction.user.roles:
            return await interaction.followup.send("You have already verified here.")

        if role is None:
            return await interaction.followup.send(
                "I can't find the appropriate role to give you. Please alert one of the moderators here.",
                ephemeral=True,
            )

        if not role.is_assignable():
            return await interaction.followup.send(
                "I've found the role to give you, but I lack the permissions to assign it to you. Please elert one of the moderators here."
            )

        await interaction.user.add_roles(  # type: ignore
            role, reason=f"Authenticated via {interaction.guild.me.name}"
        )

        return await interaction.followup.send(
            f"Authenticated! I've assigned the {role.mention} role to you!",
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx: commands.Context["AuthBot"], role: discord.Role):
        assert ctx.guild is not None

        async with ctx.typing():
            async with ctx.bot.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO guilds VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET authenticated_role = $2",
                    ctx.guild.id,
                    role.id,
                )

        await ctx.reply(
            f"Configured {role.mention} as the authenticated role on this server.",
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @app_commands.command()
    @app_commands.guild_only()
    @app_commands.guild_install()
    async def invokeauth(self, interaction: discord.Interaction):
        interaction.client.dispatch("member_join", interaction.user)
        await interaction.response.send_message("Check your DMs!", ephemeral=True)


async def setup(bot: "AuthBot"):
    await bot.add_cog(CommandsCog())
