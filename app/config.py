from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_password: str = "12345" # This sets the default value of the database_password attribute to "12345". If the DATABASE_PASSWORD environment variable is not set, it will use "12345" as the default value.
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"
        # env_file_encoding = "utf-8"


settings = Settings() # This creates an instance of the Settings class, which will automatically load the configuration values from the .env file and make them accessible through the settings object. You can then use settings.host, settings.database, settings.user, and settings.password to access the respective configuration values in your application.

# pip install python-dotenv pydantic-settings # To install the required packages for loading environment variables from a .env file and managing application settings using Pydantic.

