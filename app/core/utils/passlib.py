from passlib.context import CryptContext

crypt_content = CryptContext(schemes=["bcrypt"], deprecated="auto")
