from fastapi import FastAPI

from service.admin.router import admin_user_router


class AdminMain:
    """admin router 설정"""

    @staticmethod
    def set_router(app: FastAPI):
        app.include_router(admin_user_router.router)
