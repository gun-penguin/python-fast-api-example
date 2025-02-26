from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecretUtil:
    """보안 관련 클래스"""

    @staticmethod
    def get_password_hash(password):
        return bcrypt_context.hash(password)
