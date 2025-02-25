from fastapi import FastAPI
from app.routes import router
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI(title="User Microservice", template_folder='app/frontend/templates')
app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

