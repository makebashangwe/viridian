from fastapi import FastAPI

from routers import (
    auth_route,
    activities,
    sessions,
    xp,
    goals,
    rewards
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_route.router)
app.include_router(activities.router)
app.include_router(sessions.router)
app.include_router(xp.router)
app.include_router(goals.router)
app.include_router(rewards.router)


@app.get("/")
def read_root():
    return {"message": "Viridian API is running"}