from fastapi import APIRouter, Query

from libs.common.response.response_data_model import ResponseDataModel
from libs.common.response.response_list_model import ResponseListModel
from libs.common.response.response_model import ResponseModel
from libs.common.schema.page_base_schema import PageBaseSchema
from service.app.schema.app_user_schema import AppUserSchema
from service.app.service.app_user_service import AppUserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/", response_model=ResponseListModel[AppUserSchema])
async def get_user_list(page: int = Query(1, ge=1),
                        size: int = Query(10, ge=1, le=100)):
    param = PageBaseSchema()
    param.page = page
    param.size = size

    result = ResponseListModel()
    result.count = await AppUserService.get_user_count()
    if result.count > 0:
        result.list = await AppUserService.get_user_list(param)
    return result


@router.get("/{item_id}", response_model=ResponseDataModel[AppUserSchema])
async def get_user(item_id: int):
    result = ResponseDataModel()
    result.data = await AppUserService.get_user(item_id)
    return result


@router.post("/", response_model=ResponseModel)
async def create_user(user: AppUserSchema):
    service_result = await AppUserService.create_user(user)
    result = ResponseModel()
    result.code = 1 if service_result else False
    return result
