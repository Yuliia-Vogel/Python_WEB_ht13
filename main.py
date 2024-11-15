import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse # для обсл.favicon.ico

from src.routes import contacts, auth, users
from src.conf.config import settings

app = FastAPI()

# щоб не випадало повідомлення "GET /favicon.ico HTTP/1.1" 404 Not Found:
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("favicon.ico")

# Визначаємо список дозволених джерел
origins = [ 
    "http://localhost:3000"
    ]

# Додаємо CORSMiddleware у застосунок
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api') # для включення маршрутизації, визначеної в модулі contacts
app.include_router(users.router, prefix='/api')

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(r)


@app.get("/")
def root():
    return {"message": "Welcome to my homework 13"}