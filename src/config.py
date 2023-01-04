from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PowerDrive"
    db_host: str = "db"
    db_port: str = "5432"
    db_user: str = "powerdrive"
    db_password: str = "powerdrive"
    db_name: str = "powerdrive"
    test_db_name: str = "powerdrive_test"

    db_url: str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    test_db_url: str = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{test_db_name}"

    root_path: str = "/"
