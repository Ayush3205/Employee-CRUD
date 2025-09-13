from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import connect_to_mongo, close_mongo_connection
from router import router as employee_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Employee Management API",
    description="A FastAPI application for managing employees with MongoDB",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(employee_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)