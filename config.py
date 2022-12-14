from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "PowerDrive"
    db_host: str = "yuumi.skni.umcs.pl"
    db_port: str = "54320"
    db_user: str = "postgres"
    db_password: str = "KI5xTWZXhGT4Wv2vsKNrh6JeToHqp2g44n3XB4lD"
    db_name: str = "postgres"
    db_url: str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" #TODO trzeba sie podlaczyc do bazy
    root_path: str = "/"
