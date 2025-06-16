import aiohttp
import asyncpg
import uvloop

from bot import AuthBot
import config


async def main():
    async with (
        aiohttp.ClientSession() as session,
        asyncpg.create_pool(config.DATABASE_URL) as pool,
    ):
        bot = AuthBot(session, pool)
        await bot.start(config.TOKEN)


if __name__ == "__main__":
    uvloop.run(main())
