from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import discord
from discord.ext import commands

if TYPE_CHECKING:
    import aiohttp
    import asyncpg


COGS = {"jishaku", "cogs.events", "cogs.emails", "cogs.commands"}


class AuthBot(commands.Bot):
    def __init__(self, session: aiohttp.ClientSession, pool: asyncpg.Pool):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix="!",
            intents=intents,
        )

        self.session = session
        self.pool = pool
        discord.utils.setup_logging(level=logging.INFO)

    async def setup_hook(self):
        for cog in COGS:
            await self.load_extension(cog)
            logging.debug(f"Loaded {cog}")

        logging.debug("Attempting to sync application commands...")
        await self.tree.sync()
        logging.info("Application commands synced!")
