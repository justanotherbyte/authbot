from typing import TYPE_CHECKING

import discord
from discord import ui

import config

if TYPE_CHECKING:
    from bot import AuthBot
    from cogs.emails import EmailQueue


class EmailModal(ui.Modal, title="Email Verification"):
    email = ui.TextInput(
        label="Email", placeholder=f"Enter your {config.INSTITUTE_NAME} email"
    )

    async def on_submit(self, interaction: discord.Interaction):
        emails_cog: "EmailQueue" = interaction.client.get_cog("EmailQueue")  # type: ignore
        await emails_cog.email_queue.put((interaction.user.id, self.email.value))
        await interaction.response.send_message(f"Email: {self.email.value}")


class CodeModal(ui.Modal, title="Code Verification"):
    code = ui.TextInput(label="Code", placeholder="Enter your verification code")

    async def on_submit(self, interaction: discord.Interaction["AuthBot"]):
        await interaction.response.defer(ephemeral=True, thinking=True)

        emails_cog: EmailQueue = interaction.client.get_cog("EmailQueue")  # type: ignore

        async with interaction.client.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM authenticated_users WHERE user_id = $1",
                interaction.user.id,
            )

        if row is not None:
            await interaction.followup.send("You are already authenticated.")

        user_code = self.code.value
        actual_code = emails_cog.codes.get(interaction.user.id)
        if actual_code is None:
            await interaction.response.send_message(
                "Click the first button to get a code", ephemeral=True
            )
        elif user_code != actual_code:
            await interaction.response.send_message("Incorrect code", ephemeral=True)
        else:
            async with interaction.client.pool.acquire() as conn:
                await conn.execute(
                    "INSERT INTO authenticated_users VALUES($1)", interaction.user.id
                )

            assert interaction.guild is not None
            await interaction.followup.send(
                (
                    "Verified! Run the `/verify` command in any guild to authenticate. "
                    "You will be automatically authenticated the next time you join a guild "
                    f"protected by {interaction.guild.name}."
                )
            )


class VerifyCTA(ui.View):
    @ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify")
    async def verify(self, interaction: discord.Interaction["AuthBot"], _: ui.Button):
        await interaction.response.send_modal(EmailModal())

    @ui.button(label="Enter Code", style=discord.ButtonStyle.secondary)
    async def enter_code(
        self, interaction: discord.Interaction["AuthBot"], _: ui.Button
    ):
        await interaction.response.send_modal(CodeModal())
