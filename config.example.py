# !!!!! RENAME THIS FILE TO config.py !!!!!!

# Discord
TOKEN = "<YOUR DISCORD TOKEN HERE>"  # Your Discord Bot Token

# Gmail
EMAIL_USERNAME = (
    "youremail@gmail.com"  # The email you'd like to send the code emails from.
)
EMAIL_PASSWORD = "Gmail App Password"  # The password to use to authenticate with the SMTP server. If this is Gmail, enable 2FA and use an App Password.
EMAIL_HOSTNAME = "smtp.gmail.com"  # Email host domain
EMAIL_PORT = 587

# PostgreSQL
DATABASE_URL = "postgresql://[username]:[password]@[host]:[port]/[db name]"  # postgres connection uri

# Functionality
## Emails
WELCOME_MESSAGE = (
    "Hi. $MENTION I'm AuthBot. Welcome to $GUILD_NAME. "
    "Please use the below buttons to authenticate yourself."
)  # this is sent to the user directly in private messages when the user joins your guild.

INSTITUTE_NAME = "University Name"
EMAIL_SUBJECT = "Welcome to the University's Discord Eco-system"  # the subject of the auth code email.

## Codes
CODE_SIZE = 5  # the size of codes. 5 is a pretty good number. There are 52521875 possible codes.
CODE_POOL = "0123456789abcdefghijklmopqrstuvwxyz"  # the character pool that codes are generated from.
EMAIL_HTML_TEMPLATE = "templates/email.html"
EMAIL_TEXT_TEMPLATE = "templates/email.txt"


def CHECK_EMAIL(email: str) -> bool:
    return email.endswith(".ed.ac.uk")
