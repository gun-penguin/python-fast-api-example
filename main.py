import sys
import uvicorn
import time

from pathlib import Path
from fastapi import Request, FastAPI

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
from libs.common.type.service_type import ServiceType
from libs.common.util.env_util import EnvUtil
from libs.common.exception.common_exception import CommonException
from libs.db.config.db_config import DbConfig

if len(sys.argv) <= 1:
    print("서비스 종류 확인")
    exit(1)

service_type = ServiceType(sys.argv[1])
EnvUtil.set_env(str(Path.cwd()), service_type)
DbConfig.init()

if EnvUtil.is_swagger():
    app = FastAPI()
else:
    app = FastAPI(docs_url=None,
                  redoc_url=None,
                  openapi_url=None)

if service_type == ServiceType.APP:
    from service.app.app_main import AppMain

    AppMain.set_router(app)
elif service_type == ServiceType.ADMIN:
    from service.admin.admin_main import AdminMain

    AdminMain.set_router(app)

if app is not None:
    @app.middleware("http")
    async def exception_middleware(request: Request, call_next):
        """예외 사항 처리"""
        try:
            return await call_next(request)
        except CommonException as e:
            EnvUtil.print_exc()
            return JSONResponse(
                status_code=200,
                content={"code": e.code, "msg": request.url.path + " => " + e.msg}
            )
        except Exception as e:
            EnvUtil.print_exc()
            return JSONResponse(
                status_code=200,
                content={"code": 500, "msg": request.url.path + " => " + str(e)}
            )


    @app.middleware("http")
    async def time_check_middleware(request: Request, call_next):
        """실행 시간 체크"""
        start_time = time.time()
        res = await call_next(request)
        process_time = time.time() - start_time
        # 실행 시간이 3초 이상
        if process_time >= 3:
            print("실행 시간=>" + str(process_time) + 'ms')
        return res


    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """http 에러 처리"""
        print('http error')
        if exc.status_code == 404:
            return JSONResponse(
                status_code=200,
                content={"code": 404, "msg": request.url.path + "찾을 수 없음"}
            )
        return JSONResponse(
            status_code=200,
            content={"code": exc.status_code, "msg": str(exc.detail)}
        )


    @app.exception_handler(RequestValidationError)
    async def valid_exception_handler(request: Request, exc: RequestValidationError):
        """RequestValidationError 처리"""
        EnvUtil.print_exc()
        return JSONResponse(
            status_code=200,
            content={"code": 1, "msg": request.url.path + " => " + str(exc)}
        )


    uvicorn.run(app, host="0.0.0.0", port=EnvUtil.get_port())
else:
    print("서비스 시작 실패")
