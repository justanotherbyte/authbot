# Discord
TOKEN = "<YOUR DISCORD TOKEN HERE>"

# Gmail
EMAIL_USERNAME = "youremail@gmail.com"
EMAIL_PASSWORD = "Gmail App Password"
EMAIL_HOSTNAME = "smtp.gmail.com"
EMAIL_PORT = 587

# PostgreSQL
DATABASE_URL = "postgresql://postgres:authbot@localhost:5432/postgres"

# Functionality
## Emails
WELCOME_MESSAGE = (
    "Hi. $MENTION I'm AuthBot. Welcome to $GUILD_NAME. "
    "Please use the below buttons to authenticate yourself."
)
INSTITUTE_NAME = "University Name"
EMAIL_SUBJECT = "Welcome to the University's Discord Eco-system"

## Codes
CODE_SIZE = 5
CODE_POOL = "0123456789abcdefghijklmopqrstuvwxyz"
EMAIL_HTML_TEMPLATE = "templates/email.html"
EMAIL_TEXT_TEMPLATE = "templates/email.txt"

## Discord
AUTHENTICATED_ROLE_ID = 123456789


def CHECK_EMAIL(email: str) -> bool:
    return email.endswith(".ed.ac.uk")
