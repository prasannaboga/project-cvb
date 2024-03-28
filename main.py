from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from project_ai_gemini.config.settings import Settings

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

settings = Settings()

@app.get("/")
async def root():
  return {
      "message": "Hello World!",
      "environment": settings.ENVIRONMENT
  }


if __name__ == "__main__":
  import uvicorn
  uvicorn.run("main:app", host="0.0.0.0", port=8010)
