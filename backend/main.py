from fastapi import FastAPI
from database import engine
import db_models

from routers import (
    auth_route,
    activities,
    sessions,
    xp,
    goals,
    rewards
)


app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)

app.include_router(auth_route.router)
app.include_router(activities.router)
app.include_router(sessions.router)
app.include_router(xp.router)
app.include_router(goals.router)
app.include_router(rewards.router)


@app.get("/")
def read_root():
    return {"message": "Viridian API is running"}