import environ

env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

DEFAULT_TTL = 60 * 60 * 4
ADMIN_USERNAME = env("ADMIN_USERNAME", default="admin")
ADMIN_PASSWORD = env("ADMIN_PASSWORD", default="admin")
ADMIN_EMAIL = env("ADMIN_PASSWORD", default="admin@admin.com")
