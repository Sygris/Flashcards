from passlib.context import CryptContext


# Class that handles password hashing and checks if plain password matches the hashed password
class HashHelper:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    # Staticmethod so there is no need to create an instance of HashHelper
    @staticmethod
    def hash_password(password: str) -> str:
        return HashHelper.pwd_context.hash(password)

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return HashHelper.pwd_context.verify(password, hashed)
