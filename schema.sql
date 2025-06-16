CREATE TABLE IF NOT EXISTS authenticated_users (
    user_id BIGINT PRIMARY KEY,
    authenticated_at TIMESTAMP CURRENT_TIMESTAMP()
)

CREATE TABLE IF NOT EXISTS guilds (
    guild_id BIGINT PRIMARY KEY,
    authenticated_role BIGINT UNIQUE NOT NULL
)