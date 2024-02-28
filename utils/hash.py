from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Encryption():
    @staticmethod
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

    @staticmethod
    def check_pw(hashed_password, plain_password):
        return pwd_cxt.verify(plain_password, hashed_password)
