from passlib.context import CryptContext

hash_algorithm = CryptContext(schemes=["bcrypt"], deprecated="auto")
