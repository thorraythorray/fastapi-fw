from passlib.context import CryptContext

crypte_content = CryptContext(schemes=["bcrypt"], deprecated="auto")
