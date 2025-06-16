import asyncio
import logging
import random
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import TYPE_CHECKING

import aiosmtplib
from discord.ext import commands, tasks

import config

if TYPE_CHECKING:
    from bot import AuthBot


class EmailQueue(commands.Cog):
    def __init__(self, bot: "AuthBot"):
        self.email_queue = asyncio.Queue()
        self.smtp_client = aiosmtplib.SMTP(
            hostname=config.EMAIL_HOSTNAME,
            port=config.EMAIL_PORT,
            use_tls=False,
            username=config.EMAIL_USERNAME,
            password=config.EMAIL_PASSWORD,
        )
        self.send_emails.start()
        self.rand = random.SystemRandom()

        self.codes: dict[int, str] = {}
        self.bot = bot

        with open(config.EMAIL_HTML_TEMPLATE, "r") as f:
            self.html_template = Template(f.read())

        with open(config.EMAIL_TEXT_TEMPLATE, "r") as f:
            self.text_template = Template(f.read())

    def _generate_verification_code(self, member_id: int) -> str:
        code = "".join(self.rand.choices(config.CODE_POOL, k=config.CODE_SIZE))
        self.codes[member_id] = code

        return code

    async def cog_unload(self) -> None:
        self.send_emails.stop()

    @tasks.loop(seconds=15)
    async def send_emails(self):
        logging.debug("Email Loop start")
        coros = []
        while not self.email_queue.empty():
            user_id, email = await self.email_queue.get()
            code = self._generate_verification_code(user_id)

            message = MIMEMultipart("alternative")
            message["From"] = config.EMAIL_USERNAME
            message["To"] = email
            message["Subject"] = config.EMAIL_SUBJECT

            context = {
                "CODE": code,
                "DISCORD_USER_ID": user_id,
                "EMAIL": email,
                "INSTITUTE": config.INSTITUTE_NAME,
                "BOT_NAME": self.bot.user.name,  # type: ignore
            }

            text_content = self.text_template.safe_substitute(**context)
            html_content = self.html_template.safe_substitute(**context)

            message.attach(MIMEText(text_content, "plain"))
            message.attach(MIMEText(html_content, "html"))

            coro = self.smtp_client.send_message(message)
            coros.append(coro)

        await asyncio.gather(*coros)

    @send_emails.before_loop
    async def connect_smtp(self):
        logging.info("Connecting SMTP client")
        await self.smtp_client.connect()
        logging.info("SMTP client connected")


async def setup(bot: "AuthBot"):
    await bot.add_cog(EmailQueue(bot))
