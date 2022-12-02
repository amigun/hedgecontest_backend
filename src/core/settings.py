from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite:///database.sqlite3'
    authjwt_secret_key: str = 'A2#37mjWI44O'
