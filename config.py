from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PowerDrive"
    db_host: str = "db"
    db_port: str = "3306"
    db_user: str = "skrzat"
    db_password: str = "skrzat"
    db_name: str = "skrzat"
    db_url: str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    root_path: str = "/"
