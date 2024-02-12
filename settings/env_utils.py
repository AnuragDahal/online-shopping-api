import os
from dotenv import load_dotenv

load_dotenv()


class Environment():

    def __init__(self):
        self.DATABASE_URL = os.environ.get("DATABASE_URL")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.environ.get("Access_Token_Expire_Minutes"))
        self.secret_key = os.environ.get("SECRET_KEY")
        self.ALGORITHM = os.environ.get("ALGORITHM")
        self.INVALID_CREDENTIALS = "Invalid Credentials"
        self.TOKEN_TYPE = "bearer"
        self.TOKEN_KEY = "token"
        self.TESTDATABASE_URL = os.environ.get("TEST_DATABASE_URL")
