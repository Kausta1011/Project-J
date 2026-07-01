from passlib.context import CryptContext

hash_pwd = CryptContext(schemes= ["bcrypt"], )

def hash_password(password : str)-> str:
    return hash_pwd.hash(password)