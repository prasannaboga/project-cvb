from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from project_cvb.app.api import api_router
from project_cvb.config.mongodb_config import initialize_mongodb
from project_cvb.config.settings import Settings

app = FastAPI()
app.include_router(api_router, prefix="/api")
app.mount("/public", StaticFiles(directory="public"), name="public")


settings = Settings()
initialize_mongodb()


@app.get("/", tags=["root"])
async def root():
  return {
      "message": "Hello World!",
      "environment": settings.ENVIRONMENT
  }


if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="0.0.0.0", port=8010)
