from fastapi import FastAPI

from service.app.router import app_user_router


class AppMain:
    """app router 설정"""

    @staticmethod
    def set_router(app: FastAPI):
        app.include_router(app_user_router.router)
