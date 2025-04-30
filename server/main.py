from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from server.database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行的代码
    Base.metadata.create_all(bind=engine)
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

app.include_router(user_router)
app.include_router(auth_router)