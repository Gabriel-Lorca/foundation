from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from server.database import engine, Base


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    # 启动时执行的代码
    from server.db_init import initialize_database
    initialize_database(engine.url, Base)
    # 使用fastapi_app参数
    fastapi_app.state.database_initialized = True

    yield
    # 关闭时执行的代码

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    )

from server.routers.user import router as user_router
from server.routers.auth import router as auth_router
from server.routers.role import router as role_router
from server.routers.menu import router as menu_router

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(role_router)
app.include_router(menu_router)
