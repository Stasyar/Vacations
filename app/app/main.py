from fastapi import FastAPI

from app.app import routers
from app.db import database, models

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

app.include_router(routers.router, prefix="/vacations")
