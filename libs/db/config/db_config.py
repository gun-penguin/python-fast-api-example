from functools import wraps

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from libs.common.type.stage_type import StageType
from libs.common.util.env_util import EnvUtil


class DbConfig:
    write_engine = None
    read_engine = None
    async_write_session = None
    async_read_session = None
    db_model_base = None

    @staticmethod
    def init():
        # SQLAlchemy 사용할 DB URL
        db_url = EnvUtil.get_db_url()
        db_schema = EnvUtil.get_db_schema()
        is_sql_show = EnvUtil.get_db_sql_show()

        # SQLAlchemy engine
        DbConfig.write_engine = create_async_engine(db_url,
                                                    pool_size=10, max_overflow=10, pool_timeout=30,
                                                    echo=is_sql_show,
                                                    pool_recycle=1800)
        DbConfig.read_engine = create_async_engine(db_url,
                                                   pool_size=10, max_overflow=10, pool_timeout=30,
                                                   pool_recycle=1800, echo=is_sql_show,
                                                   execution_options={"readonly": True})

        # DB 세션
        DbConfig.async_write_session = async_sessionmaker(bind=DbConfig.write_engine,
                                                          autocommit=False, autoflush=False,
                                                          expire_on_commit=False)
        DbConfig.async_read_session = async_sessionmaker(bind=DbConfig.read_engine, autocommit=False,
                                                         autoflush=False,
                                                         expire_on_commit=False)

        # Base class
        metadata = MetaData(schema=db_schema)
        DbConfig.db_model_base = declarative_base(metadata=metadata)

    @staticmethod
    async def get_db(read_only=False):
        if read_only:
            async with DbConfig.async_read_session() as session:
                yield session
        else:
            async with DbConfig.async_write_session() as session:
                yield session


def transactional(readonly=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async for db_session in DbConfig.get_db(readonly):
                try:
                    result = await func(*args, **kwargs, db=db_session)
                    if not readonly:
                        await db_session.commit()
                    return result
                except Exception as e:
                    await db_session.rollback()
                    raise e
                finally:
                    await db_session.close()

        return wrapper

    return decorator
