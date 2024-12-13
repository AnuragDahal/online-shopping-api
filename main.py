from fastapi import FastAPI
from settings import database
from models import models
from routes import orders, users, admin, auth
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager
import asyncio
from sqlalchemy import text


@asynccontextmanager
async def lifespan(app: FastAPI):
    while True:
        try:
            # Try to create a new session to check if the database is ready
            db = next(database.get_db())
            db.execute(text('SELECT 1'))
            break
        except OperationalError:
            print("Database is not ready yet, waiting...")
            await asyncio.sleep(1)

    # Initialize the database
    models.Base.metadata.create_all(bind=database.engine)
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Shopping Cart Api"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Shopping Cart API.Navigate to /docs to use the API via swagger"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(admin.router)
