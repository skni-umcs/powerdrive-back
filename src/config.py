from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PowerDrive"
    root_path: str = "/"

    db_host: str = "db"
    db_port: str = "5432"
    db_user: str = "powerdrive"
    db_password: str = "powerdrive"
    db_name: str = "powerdrive"

    base_file_path: str = "/files/"
    base_file_path_trash: str = "/files/trash/"

    @property
    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_prefix = "PD_"
