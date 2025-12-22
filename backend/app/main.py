from fastapi import FastAPI
from backend.app.database import init_db
from backend.app.nutrition.routes.nutrition import router as nutrition_router

app = FastAPI(title="FitLab API")

app.include_router(nutrition_router)

@app.on_event("startup")
def on_startup():
    init_db()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)