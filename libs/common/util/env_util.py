import os
import traceback

from libs.common.type.service_type import ServiceType
from libs.common.type.env_key_type import EnvKeyType
from libs.common.type.stage_type import StageType
from dotenv import load_dotenv


class EnvUtil:
    """환경 변수 클래스"""
    root_path: str
    service_type: ServiceType
    stage_type: StageType

    @staticmethod
    def set_env(root_path: str, service_type: ServiceType):
        EnvUtil.root_path = root_path
        EnvUtil.service_type = service_type
        load_dotenv(os.path.join(EnvUtil.root_path, "env" + os.sep + ".env_" + str(EnvUtil.service_type.value)))
        EnvUtil.stage_type = StageType(os.getenv(EnvKeyType.STAGE.value))

    @staticmethod
    def get_value(name: str):
        return os.getenv(name)

    @staticmethod
    def get_port():
        return int(os.getenv(EnvKeyType.PORT.value))

    @staticmethod
    def get_db_url():
        return os.getenv(EnvKeyType.DB_URL.value)

    @staticmethod
    def get_db_schema():
        return os.getenv(EnvKeyType.DB_SCHEMA.value)

    @staticmethod
    def get_db_sql_show():
        show = os.getenv(EnvKeyType.DB_SQL_SHOW.value)

        if show == 'true':
            return True

        return False

    @staticmethod
    def get_access_key():
        return os.getenv(EnvKeyType.ACCESS_KEY.value)

    @staticmethod
    def print_exc():
        traceback.print_exc()

    @staticmethod
    def is_swagger() -> bool:
        if EnvUtil.stage_type == StageType.PROD:
            return False
        return True
