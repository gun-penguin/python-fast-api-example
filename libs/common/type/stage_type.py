from enum import Enum

class StageType(Enum):
    """실행 상태 enum"""
    DEV = 'dev'
    QA = 'qa'
    PROD = 'prod'
