from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from fastapi import FastAPI
from routers import user_router, game_router, payment_router
from kafka_manager import consuming
import asyncio

@asynccontextmanager
async def lifespan(app:FastAPI):
    #await delete_tables() # вернуть если нужно отчистить бд
    #print('DB is cleaned')
    await create_tables()
    print('DB is redy')

    asyncio.create_task(consuming())

    yield
    print('Turning off...')

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(game_router)
app.include_router(payment_router)