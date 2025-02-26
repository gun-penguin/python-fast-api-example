from enum import Enum

class EnvKeyType(Enum):
    """환경 변수 키 enum"""
    PORT = 'PORT'
    STAGE = 'STAGE'
    DB_URL = 'DB_URL'
    DB_SCHEMA = 'DB_SCHEMA'
    DB_SQL_SHOW = 'DB_SQL_SHOW'
    ACCESS_KEY = 'ACCESS_KEY'