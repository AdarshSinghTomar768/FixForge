from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Autonomous DevOps Agent")

app.include_router(router)
