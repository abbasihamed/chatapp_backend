from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mychat.src.routers import users,web_socket


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(web_socket.router)